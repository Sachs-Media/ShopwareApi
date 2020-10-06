import requests
import time
from shopwareapi.utils.cache import token_cache
from shopwareapi.models import Product, Currency, Category, Tax, Manufacturer
import json
import logging

log = logging.getLogger("swclient")


class ShopwareClient:

    def __init__(self, base_url, version, client_id, client_secret):
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._authorization = None
        self._version = version

    def _default_header(self):
        return {
            "Authorization": "Bearer {}".format(self._get_token()),
            "Content-Type": "application/json"
        }

    @token_cache
    def _get_token(self):
        response = requests.post(self.build_url(version=False, model="oauth/token"), data={
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret
        })
        self._authorization = {"response": response.json(), "t": time.time() }
        data = response.json()
        if "access_token" not in data:
            log.info(data)
        return data.get("access_token", None)

    def build_url(self, base_url=None, version=None, model=None, **kwargs):
        """
            Build a url used for Request by given arguments
            :param base_url: Custom URL that should be requested; If None the ShopwareClient base_url attribute would be used
            :param version: Custom API Version which should be used; If None the ShopwareClient version attribute would be used
            :param model: Required. Model which should be used for Request
            :return:
        """
        if base_url is None:
            base_url = self._base_url

        if version is None:
            version = self._version+"/"
        elif version is not False:
            version = version+"/"
        else:
            version = ""

        assert model is not None

        if type(model) in [list, tuple]:
            model = "/".join(model)

        query = "?"
        for key, value in kwargs.items():
            query += "{}={}&".format(key, value)
        if query == "?":
            query = ""

        url = "{base_url}/api/{version}{model}{query}".format(base_url=base_url, version=version, model=model, query=query)
        return url

    def post(self, url, data=None, files=None, headers=None):
        header = self._default_header()
        if headers is not None:
            header.update(headers)
        response = requests.post(url, data=json.dumps(data), headers=header, files=files)
        return self.postprocessing(response)

    def get(self, url):

        header = self._default_header()

        if header is not None:
            header.update(header)
        
        response = requests.get(url, headers=header)
        return self.postprocessing(response)

    def patch(self, url, data=None, files=None, headers=None):
        header = self._default_header()

        if header is not None:
            header.update(header)
        response = requests.patch(url, data=json.dumps(data), headers=header, files=files)
        return self.postprocessing(response)

    def postprocessing(self, response):
        if 299 <= response.status_code >= 200:
            log.debug(response.request.body)
            log.debug(response.text)
            raise ValueError("This is not a valid request. Statuscode %s" % str(response.status_code))

        try:
            if response.text != "":
                return response.json()
        except json.decoder.JSONDecodeError as e:
            log.debug(response.text)
            raise e

    @property
    def controller(self):
        return ShopwareClient.Controller(self)

    class Controller:
        def __init__(self, client):
            self.Product = Product(options={"client": client}).controller
            self.Currency = Currency(options={"client": client}).controller
            self.Category = Category(options={"client": client}).controller
            self.Tax = Tax(options={"client": client}).controller
            self.Manufacturer = Manufacturer(options={"client": client}).controller
