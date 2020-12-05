from shopwareapi.core.field import BaseField


class NumberField(BaseField):

    def __init__(self, verbose_name=None, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "NumberField"

    def to_python(self, value):
        if self.null is True and value is None:
            return None

        try:
            return int(value)
        except (AttributeError, ValueError, TypeError):
            raise ValueError("Invalid value '{}' in {} for NumberField".format(self.name, value))
