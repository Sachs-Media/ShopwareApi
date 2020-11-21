import logging

from shopwareapi.exceptions import ConfigurationError, FronzenConfigurationError

log = logging.getLogger(__name__)


class DefaultConfiguration:
    """
        Contains all default values used for this lib.
        You can modify this Values at ShopwareClient Object creation (use kwargs)
    """

    #: Time span in which a new token is already requested before the old token has expired
    #: Time in minutes
    TOKEN_EXPIRE_RENEW_THRESHOLD = 60
    #: URL with protocol to the store
    #: Only the protocol and domain is allowed (ports also) but no path/parameter/query/fragments
    API_BASE_URL = None
    #: oAuth2 Credential. This can be created at Integrations or at salesChannel
    CLIENT_ID = None
    #: oAuth2 Credential. This can be created at Integrations or at salesChannel
    CLIENT_SECRET = None
    #: API version which should be used. it can be v2 or v3
    API_VERSION = None
    #: timeout for every http api request.
    REQUEST_TIMEOUT = 30


class Configuration(object):
    """
        This object contains the resulting Configuration from given custom Configuration and
        default Configuration. Access the values via Attribute call
    """
    defaults = DefaultConfiguration()
    _frozen = False

    def __init__(self, **kwargs):
        """
            Initialize Configuration object
            first loads the default values into the object, and then overwrites them with your own values
            Own values can be defined with the kwargs.
            the key must correspond to a value from the default values

            :param kwargs: Customized configuration values
        """
        # If this object is forzen no changes can be made
        default_attributes = filter(lambda item: not item.startswith("__"), dir(DefaultConfiguration))

        for config_name in default_attributes:
            config_value = getattr(self.get_defaults(), config_name.upper())
            setattr(self, config_name.upper(), config_value)
            log.debug("set config default value for {} to {}".format(config_name, config_value))

        # Use custom Configuration values
        self.update(**kwargs)

    def __setattr__(self, key, value):
        """
            Prevent setattr if the object was frozen
        """
        if not hasattr(Configuration, "_frozen"):
            return super(Configuration, self).__setattr__(key, value)

        if not self._frozen:
            return super(Configuration, self).__setattr__(key, value)
        else:
            raise FronzenConfigurationError("The configuration settings are frozen. No changes are allowed")

    @classmethod
    def get_defaults(cls) -> DefaultConfiguration:
        """
            Returns the dict of default values

            :return DefaultConfiguration: Object that contains every possible configuration and its default value
        """
        return cls.defaults

    def update(self, **kwargs):
        """
            Updates this object with custom Configuration settings given by kwargs

            :param kwargs: every allowed (and in DefaultConfiguration defined) key value configuration parameter
            :return dict: Changed parameters only
        """
        if not self._frozen:
            updated_configurations = {}
            for config_name, config_value in kwargs.items():

                if hasattr(self.get_defaults(), config_name.upper()):
                    if getattr(self, config_name.upper()) != config_value:
                        log.debug("set config value for {} to {}".format(config_name, config_value))
                        updated_configurations[config_name.upper()] = config_value
                        setattr(self, config_name.upper(), config_value)
                else:
                    raise ConfigurationError("{} isnt a configurable parameter".format(config_name))
        else:
            raise FronzenConfigurationError("The configuration settings are frozen. No changes are allowed")

    def freeze(self):
        """
            Activate freeze of Configuration object
        """
        self._frozen = True


settings = Configuration()
