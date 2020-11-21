from unittest import TestCase
from unittest.mock import patch, Mock
from shopwareapi import ShopwareClient
from shopwareapi import exceptions
from shopwareapi.utils.conf import settings


class TestShopwareClient(TestCase):


    def test_client_configuration(self):
        client = ShopwareClient(api_base_url="https://www.test.de", api_version="v3")

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*define.*scheme") as e:
            client._validate_configuration({"api_base_url": "test.de"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*define.*scheme"):
            client._validate_configuration({"api_base_url": "test.de/asdf"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no path"):
            client._validate_configuration({"api_base_url": "https://test.de/asdf"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no query"):
            client._validate_configuration({"api_base_url": "https://test.de?asdf=Asdf"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no params"):
            client._validate_configuration({"api_base_url": "https://test.de/;test=abc"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no query"):
            client._validate_configuration({"api_base_url": "https://test.de?asdf=Asdf;foo=bar"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no path"):
            client._validate_configuration({"api_base_url": "https://test.de/asdf/?test=asdf"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*no fragment"):
            client._validate_configuration({"api_base_url": "https://test.de#asdf"})

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid"):
            client = ShopwareClient()

        with self.assertRaisesRegex(exceptions.ConfigurationValueError, "given value.*is invalid.*Allowed.*v2.*v3"):
            client._validate_configuration({"api_base_url": "https://localhost", "api_version": "asdf"})

    def test_apiversion(self):
        client = ShopwareClient(api_base_url="https://www.example.com", api_version="v2")
        self.assertEqual(settings.API_BASE_URL, "https://www.example.com")
        self.assertEqual(settings.API_VERSION, "v2")
        client = ShopwareClient(api_base_url="https://www.example.com", api_version="v3")
        self.assertEqual(settings.API_BASE_URL, "https://www.example.com")
        self.assertEqual(settings.API_VERSION, "v3")
        client = ShopwareClient(api_base_url="https://www.example.com:8000", api_version="v3")
        self.assertEqual(settings.API_BASE_URL, "https://www.example.com:8000")
        self.assertEqual(settings.API_VERSION, "v3")
        client = ShopwareClient(api_base_url="https://example.com:8000", api_version="v3")
        self.assertEqual(settings.API_BASE_URL, "https://example.com:8000")
        self.assertEqual(settings.API_VERSION, "v3")

    def test_okcreate(self):
        client = ShopwareClient(api_base_url="https://localhost", api_version="v2")
        self.assertEqual(settings.API_VERSION, "v2")
        self.assertEqual(settings.API_BASE_URL, "https://localhost")

    def test_default_header(self):
        client = ShopwareClient(api_base_url="https://localhost", api_version="v2")

        with patch("shopwareapi.utils.http.ShopwareClientHttpMixin._get_token", Mock(return_value="TESTTOKEN")) as e:
            self.assertEqual(dict, type(client._default_header()))

    def test_wrong_config(self):

        with self.assertRaises(exceptions.ConfigurationError):
            ShopwareClient(invalid_example=234)