from shopwareapi.client import ShopwareClient
from unittest import TestCase


class TestShopwareClientHttp(TestCase):

    def test_build_url(self):
        """
            Test the build url method
        """
        c = ShopwareClient(api_base_url="https://localhost", api_version="v3", client_id="asdf", client_secret="ASDF")

        url = c.build_url(model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v3/media/upload")

        url = c.build_url(version="v2", model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v2/media/upload")

        url = c.build_url(version="v2", model=("media", "upload"))
        self.assertEqual(url, "https://localhost/api/v2/media/upload")

        url = c.build_url(version="v2", model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v2/media/upload?test=True")

        url = c.build_url(version="v3", model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        url = c.build_url(version=False, model=("media", "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/media/upload?test=True")

        url = c.build_url(model=("media", None, "upload"), test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        url = c.build_url(model="media/upload/", test=True)
        self.assertEqual(url, "https://localhost/api/v3/media/upload?test=True")

        with self.assertRaises(AssertionError):
            url = c.build_url(test=True)
