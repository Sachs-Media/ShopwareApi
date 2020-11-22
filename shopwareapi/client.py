import logging
from urllib.parse import urlparse

from shopwareapi.exceptions import ConfigurationValueError
from shopwareapi.utils.conf import settings
from shopwareapi.utils.http import ShopwareClientHttpMixin

log = logging.getLogger(__name__)


class ShopwareClient(ShopwareClientHttpMixin):
    """
            the shopwareclient api main class
            required configuration:

            :param api_base_url: The url of shopware. (https://shopwaredomain.com)
            :param api_version: API Version. Supported are v2, v3
            :param client_id: oauth2 client ID
            :param client_secret: oauth2 client secret
        """

    def __init__(self, **kwargs):
        self._authorization = None
        self._validate_configuration(kwargs)
        settings.update(**kwargs)

    def _validate_configuration(self, orginal_config):
        """
            Validate the Configuration parameters that are given by object initializeation

            :param orginal_config: dict of config which should be checked
        """
        config = {key.lower(): value for key, value in orginal_config.items()}
        if "api_base_url" in config:
            o = urlparse(config.get("api_base_url"))

            if o.scheme is None or o.scheme == "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (please define a protocol/scheme)".format(
                        config.get("api_base_url")))

            if o.params is not None and o.params != "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (no params are allowed)".format(
                        config.get("api_base_url")))

            if o.path is not None and o.path != "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (no path are allowed)".format(
                        config.get("api_base_url")))

            if o.fragment is not None and o.fragment != "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (no fragment are allowed)".format(
                        config.get("api_base_url")))

            if o.query is not None and o.query != "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (no query are allowed)".format(
                        config.get("api_base_url")))

            if o.netloc is None or o.netloc == "":
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_base_url' is invalid. (domain are required)".format(
                        config.get("api_base_url")))
        else:
            raise ConfigurationValueError(
                "The given value '{}' for parameter 'api_base_url' is invalid".format(config.get("api_base_url")))

        if "api_version" in config:
            if config.get("api_version") not in ["v2", "v3"]:
                raise ConfigurationValueError(
                    "The given value '{}' for parameter 'api_version' is invalid. Allowed/supported versions are v2, v3".format(
                        config.get("api_version")))
