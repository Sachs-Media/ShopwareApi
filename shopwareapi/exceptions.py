
class ConfigurationError(ValueError):
    """
        Raises when the given Configuration doesnt available
    """
    pass


class FronzenConfigurationError(ConfigurationError):
    """
        Raises if changes will me made after the object is frozen
    """
    pass