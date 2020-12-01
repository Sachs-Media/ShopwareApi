from shopwareapi.core.field import BaseField


class CharField(BaseField):

    def __init__(self, verbose_name=None, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        return value
