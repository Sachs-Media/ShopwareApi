from shopwareapi.core.field import BaseField


class IntegerField(BaseField):

    def __init__(self, verbose_name=None, **kwargs):
        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "IntegerField"

    def to_python(self, value):
        try:
            return int(value)
        except (AttributeError, ValueError):
            raise ValueError("Invalid value '{}' for IntegerField".format(value))
