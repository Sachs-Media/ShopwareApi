from shopwareapi.core.field import BaseField


class BooleanField(BaseField):

    def __init__(self, verbose_name=None, **kwargs):
        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "BooleanField"

    def to_python(self, value):

        if self.null is True and value is None:
            return None

        try:
            if type(value) is bool:
                return bool(value)
            if str(value).lower() in ["1", "yes", "true", "on", "y", "t"]:
                return True
            elif str(value).lower() in ["0", "no", "false", "off", "n", "f"]:
                return False
            else:
                raise ValueError("Unidentifiable value '{}' in BooleanField".format(value))
        except (AttributeError, ValueError):
            raise ValueError("Invalid value '{}' for BooleanField {}".format(value, self.name))
