import uuid

from shopwareapi.core.field import BaseField


class UUIDField(BaseField):

    def __init__(self, verbose_name=None, **kwargs):
        kwargs['max_length'] = 32
        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "UUIDField"

    def to_python(self, value):
        if value is not None and not isinstance(value, uuid.UUID):
            input_form = 'int' if isinstance(value, int) else 'hex'
            try:
                return uuid.UUID(**{input_form: value})
            except (AttributeError, ValueError):
                raise ValueError("Invalid value '{}' for UUIDField {}".format(value, self.name))
        return value

    def to_simple(self, val):
        if isinstance(val, uuid.UUID):
            return val.hex
        else:
            return val
