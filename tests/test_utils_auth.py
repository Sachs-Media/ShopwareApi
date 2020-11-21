from unittest import TestCase
from shopwareapi import ShopwareClient
from unittest.mock import Mock, patch, PropertyMock, MagicMock
import json

class TestClientTokenCacheDecorator(TestCase):

    def setUp(self) -> None:
        self.client = ShopwareClient(api_base_url="https://test")

    def test_on_request(self):

        with patch("requests.request") as raw_request, patch("requests.post", Mock()) as raw_post:
            type(raw_post.return_value).json = Mock(return_value={"access_token": "testtoken", "expire_in": 300})
            self.client.request("get", "http://localhost")
            args, kwargs = raw_request.call_args
            headers = kwargs.get("headers")
            self.assertEqual(headers.get("Authorization"), "Bearer testtoken")
            self.assertEqual(raw_post.call_count, 1)

        with patch("requests.request") as raw_request, patch("requests.post") as raw_post:
            self.client.request("get", "http://localhost")
            args, kwargs = raw_request.call_args
            headers = kwargs.get("headers")
            self.assertEqual(headers.get("Authorization"), "Bearer testtoken")
            self.assertEqual(raw_post.call_count, 0)