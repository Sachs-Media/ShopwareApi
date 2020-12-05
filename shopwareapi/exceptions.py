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


class ParameterError(KeyError):
    """
        Raises every time when invalid get, create, find etc. parameters are provided
    """


class ObjectDoesNotExist(ValueError):
    """
        Subexception Raises when requested data not found at remote shop
        This exception will be attached to model class
    """


class MultipleObjectsReturned(ValueError):
    """
        Raises also as Subexception when too many objects returned for given request
        (get() returns multiple results)
    """
