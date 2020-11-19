class ConfigurationError(ValueError):
    """
        Raises when the given Configuration doesnt available
    """
    pass


class ConfigurationValueError(ConfigurationError):
    """
        Raises when a value is invalid for configuration
    """
    pass


class FronzenConfigurationError(ConfigurationError):
    """
        Raises if changes will me made after the object is frozen
    """
    pass


class ShopwareClientHttpError(RuntimeError):
    """
        Raises when statuscode is not 299 <= response.status_code >= 200
    """
