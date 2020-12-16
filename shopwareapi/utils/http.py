import json
import logging
import time

import requests

from shopwareapi.exceptions import ShopwareClientHttpError
from shopwareapi.utils.auth import token_cache
from shopwareapi.utils.conf import settings

log = logging.getLogger(__name__)


class ShopwareClientHttpMixin(object):

    def _default_header(self):
        """
            provides the standard header for each shopware api request
            :return dict: all default http headers
        """
        return {
            "Authorization": "Bearer {}".format(self._get_token()),
            "Content-Type": "application/json"
        }

    @token_cache
    def _get_token(self):
        """
            requests a new bearer access_token from oauth/token interface of shopware

            :return str: the resulting access_token
        """
        response = requests.post(self.build_url(version=False, model="oauth/token"), data={
            "grant_type": "client_credentials",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET
        })

        data = self.postprocessing(response)
        self._authorization = {"response": data, "t": time.time()}
        if "access_token" not in data:
            log.info(data)
        return data.get("access_token", None)

    def build_url(self, base_url=None, version=None, model=None, **kwargs):
        """
            Build a url used for Request by given arguments

            :param base_url: Custom URL that should be requested; If None the ShopwareClient base_url attribute would be used
            :type base_url: string
            :param version: Custom API Version which should be used; If None the ShopwareClient version attribute would be used
            :type version: bool,null,string
            :param model: Required. Model which should be used for Request
            :type model: list,tuple,string
            :param kwargs: Converts any kwarg to query

            :return str: fully prepared url

            :Example:

            .. code-block:: python

                from shopwareapi import ShopwareClient

                c = ShopwareClient(api_base_url="https://localhost", version="v3")

                print(c.build_url(model="media", order=desc)
                # > https://localhost/api/v3/media?order=desc

        """
        if base_url is None:
            base_url = settings.API_BASE_URL.strip("/")

        if version is None:
            version = settings.API_VERSION
        elif version is not False:
            version = version
        else:
            version = None

        assert model is not None

        query_string = ""
        query_parameter_list = []

        for key, value in kwargs.items():
            query_parameter_list.append("{}={}".format(key, value))

        if len(query_parameter_list) > 0:
            query_string = "?{}".format("&".join(query_parameter_list))

        if type(model) in [tuple, list]:
            model = list(item.strip("/") if item is not None else None for item in model)
        else:
            model = [model.strip("/")]

        url_components = list(filter(lambda i: i is not None,
                                     [base_url.strip("/"), "api", version.strip("/") if version is not None else None,
                                      *model]))
        return "/".join(url_components) + query_string

    def request(self, method, url, data=None, files=None, headers=None):
        """
            sends an generic request

            :param method: defines the HTTP Method
            :param url: dict for build_url kwargs or string as url
            :type url: str,dict
            :param data: data which should be send
            :type data: str
            :param files: files who should be uploaded
            :param headers: additional request header which should be overwritten
            :param kwargs: Parsing directly to requests libary
            :return response: Response object
        """

        request_header = self._default_header()
        if headers is not None:
            request_header.update(headers)
        elif headers is False:
            request_header = {}

        if type(url) in [dict]:
            url_string = self.build_url(**url)
        else:
            url_string = url

        log.debug("Request: {}; Data: {}".format(url, data))
        return requests.request(method,
                                url=url_string,
                                headers=request_header,
                                timeout=settings.REQUEST_TIMEOUT,
                                data=data)

    def post(self, **kwargs):
        """
            Shortcut for Post requests
            Show requests for documentation
            :func:`~request`

            :param kwargs: Request Parameters described in :func:`~request`
            :return dict: parsed packet response
        """
        response = self.request("post", **kwargs)
        return self.postprocessing(response)

    def get(self, **kwargs):
        """
            Shortcut for GET requests
            Show requests for documentation
            :func:`~request`

            :param kwargs: Request Parameters described in :func:`~request`
            :return dict: parsed packet response
        """

        response = self.request("get", **kwargs)
        return self.postprocessing(response)

    def patch(self, **kwargs):
        """
            Shortcut for PATCH requests
            Show requests for documentation
            :func:`~request`

            :param kwargs: Request Parameters described in :func:`~request`
            :return dict: parsed packet response
        """
        response = self.request("patch", **kwargs)
        return self.postprocessing(response)

    def delete(self, **kwargs):
        """
            Shortcut for DELETE requests
            Show requests for documentation
            :func:`~request`

            :param kwargs: Request Parameters described in :func:`~request`
            :return dict: parsed packet response
        """
        response = self.request("delete", **kwargs)
        return self.postprocessing(response)

    def postprocessing(self, response):
        """
            processes the http responses and parses the packet content (json)

            :param response: Response Object
            :type response: :class:`requests:requests.Response`
            :return dict: Parsed Packet content
        """
        try:
            log.debug("Response: Code: {}; Data: {}".format(response.status_code, response.text))
            if 299 <= response.status_code >= 200:
                error_response = response.json()
                for error in error_response.get("errors"):
                    log.error("{} {}".format(error.get("title"), error.get("detail")))
                log.debug("Request URL: %s " % response.request.url)
                log.debug("Request TXT: %s " % response.request.body)
                log.debug("Response TXT: %s " % response.text)
                raise ShopwareClientHttpError("Shopware returns one or multiple errors")

            if response.text != "":
                return response.json()
        except json.decoder.JSONDecodeError as e:
            log.error(response.request.__dict__)
            log.error(response.request.body)
            log.error("The shopware response isnt a Json")
            log.debug(response.text)
            raise e
