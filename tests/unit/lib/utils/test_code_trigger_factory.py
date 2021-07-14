from samcli.lib.providers.provider import ResourceIdentifier
from parameterized import parameterized
from unittest.case import TestCase
from unittest.mock import MagicMock, patch, ANY
from samcli.lib.utils.code_trigger_factory import CodeTriggerFactory


class TestCodeTriggerFactory(TestCase):
    def setUp(self):
        self.stacks = [MagicMock(), MagicMock()]
        self.factory = CodeTriggerFactory(self.stacks)

    @patch("samcli.lib.utils.code_trigger_factory.LambdaZipCodeTrigger")
    def test_create_zip_function_trigger(self, trigger_mock):
        on_code_change_mock = MagicMock()
        resource_identifier = ResourceIdentifier("Function1")
        resource = {"Properties": {"PackageType": "Zip"}}
        result = self.factory._create_lambda_trigger(resource_identifier, resource, on_code_change_mock)
        self.assertEqual(result, trigger_mock.return_value)
        trigger_mock.assert_called_once_with(resource_identifier, self.stacks, on_code_change_mock)

    @patch("samcli.lib.utils.code_trigger_factory.LambdaImageCodeTrigger")
    def test_create_image_function_trigger(self, trigger_mock):
        on_code_change_mock = MagicMock()
        resource_identifier = ResourceIdentifier("Function1")
        resource = {"Properties": {"PackageType": "Image"}}
        result = self.factory._create_lambda_trigger(resource_identifier, resource, on_code_change_mock)
        self.assertEqual(result, trigger_mock.return_value)
        trigger_mock.assert_called_once_with(resource_identifier, self.stacks, on_code_change_mock)

    @patch("samcli.lib.utils.code_trigger_factory.LambdaLayerCodeTrigger")
    def test_create_layer_trigger(self, trigger_mock):
        on_code_change_mock = MagicMock()
        resource_identifier = ResourceIdentifier("Layer1")
        result = self.factory._create_layer_trigger(resource_identifier, {}, on_code_change_mock)
        self.assertEqual(result, trigger_mock.return_value)
        trigger_mock.assert_called_once_with(resource_identifier, self.stacks, on_code_change_mock)

    @patch("samcli.lib.utils.code_trigger_factory.APIGatewayCodeTrigger")
    def test_create_api_gateway_trigger(self, trigger_mock):
        on_code_change_mock = MagicMock()
        resource_identifier = ResourceIdentifier("API1")
        result = self.factory._create_api_gateway_trigger(resource_identifier, {}, on_code_change_mock)
        self.assertEqual(result, trigger_mock.return_value)
        trigger_mock.assert_called_once_with(resource_identifier, self.stacks, on_code_change_mock)

    @patch("samcli.lib.utils.code_trigger_factory.get_resource_by_id")
    def test_create_trigger(self, get_resource_by_id_mock):
        code_trigger = MagicMock()
        resource_identifier = MagicMock()
        get_resource_by_id = MagicMock()
        get_resource_by_id_mock.return_value = get_resource_by_id
        generator_mock = MagicMock()
        generator_mock.return_value = code_trigger

        on_code_change_mock = MagicMock()

        get_generator_function_mock = MagicMock()
        get_generator_function_mock.return_value = generator_mock
        self.factory._get_generator_function = get_generator_function_mock

        result = self.factory.create_trigger(resource_identifier, on_code_change_mock)

        self.assertEqual(result, code_trigger)
        generator_mock.assert_called_once_with(
            self.factory, resource_identifier, get_resource_by_id, on_code_change_mock
        )
