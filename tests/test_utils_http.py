from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, MagicMock

from shopwareapi.client import ShopwareClient
from shopwareapi.utils.conf import settings


class TestShopwareClientHttp(TestCase):

    def setUp(self) -> None:
        self.client = ShopwareClient(api_base_url="https://localhost", api_version="v3", client_id="asdf",
                                     client_secret="ASDF")

    def test_build_url(self):
        """
            Test the build url method
        """
        url = self.client.build_url(model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v3/media/upload")

        url = self.client.build_url(version="v2", model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v2/media/upload")

        url = self.client.build_url(version="v2", model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v2/media/upload")

        url = self.client.build_url(version="v2", model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v2/media/upload?test=True")

        url = self.client.build_url(version="v3", model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        url = self.client.build_url(version=False, model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/media/upload?test=True")

        url = self.client.build_url(model=("media", None, "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        url = self.client.build_url(model="media/upload/", test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        with self.assertRaises(AssertionError):
            url = self.client.build_url(test=True)

    def test_request(self):
        """
            Test client generic request method
        """
        with patch("requests.request", Mock()) as m, patch("shopwareapi.utils.http.ShopwareClientHttpMixin._get_token",
                                                           Mock(return_value="asdf")):
            self.client.request("post",
                                url={
                                    "model": ("media"),
                                    "version": "v3"
                                },
                                data="HalloWelt")
            args, kwargs = m.call_args

            self.assertEqual(args[0], "post")
            self.assertEqual(kwargs["url"], "https://localhost/api/v3/media")
            self.assertDictEqual(kwargs["headers"], {
                'Authorization': 'Bearer asdf', 'Content-Type': 'application/json'
            })
            self.assertEqual(kwargs["timeout"], settings.REQUEST_TIMEOUT)
            self.assertEqual(kwargs["data"], "HalloWelt")

        with patch("requests.request", Mock()) as m, patch("shopwareapi.utils.http.ShopwareClientHttpMixin._get_token",
                                                           Mock(return_value="asdf")):
            self.client.request("post",
                                url="http://localhost/foobar",
                                data="HalloWelt")
            args, kwargs = m.call_args

            self.assertEqual(args[0], "post")
            self.assertEqual(kwargs["url"], "http://localhost/foobar")
            self.assertDictEqual(kwargs["headers"], {
                'Authorization': 'Bearer asdf', 'Content-Type': 'application/json'
            })
            self.assertEqual(kwargs["timeout"], settings.REQUEST_TIMEOUT)
            self.assertEqual(kwargs["data"], "HalloWelt")

    def test_request_shortcuts(self):
        """
            Test client request shortcuts (post,get,patch,delete)
        """
        with patch("shopwareapi.utils.http.ShopwareClientHttpMixin.request") as m:
            type(m.return_value).status_code = 200
            self.client.post(url="test.dde")
            args, kwargs = m.call_args
            self.assertEqual(args[0], "post")

        with patch("shopwareapi.utils.http.ShopwareClientHttpMixin.request") as m:
            type(m.return_value).status_code = 200
            self.client.get(url="test.dde")
            args, kwargs = m.call_args
            self.assertEqual(args[0], "get")

        with patch("shopwareapi.utils.http.ShopwareClientHttpMixin.request") as m:
            type(m.return_value).status_code = 200
            self.client.patch(url="test.dde")
            args, kwargs = m.call_argsks
            self.assertEqual(args[0], "patch")

        with patch("shopwareapi.utils.http.ShopwareClientHttpMixin.request") as m:
            type(m.return_value).status_code = 200
            self.client.delete(url="test.dde")
            args, kwargs = m.call_args
            self.assertEqual(args[0], "delete")
