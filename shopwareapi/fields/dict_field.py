from shopwareapi.core.field import BaseField, BaseRelationField
import json
from shopwareapi.core.model import Model
import logging

log = logging.getLogger(__name__)


class DictField(BaseField):

    def __init__(self, verbose_name=None, schema=None, **kwargs):
        self._schema = schema

        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "DictField"

    def to_python(self, value):
        return value

    def to_simple(self, value):

        if value is None:
            return {}

        result = {}
        if self._schema is None:
            for key, value in value.items():
                if type(value) in [str, int, float, bool]:
                    result[key] = value
                else:
                    raise ValueError("for more details please define a schema")
            return result
        else:
            for key, field in self._schema.items():

                if isinstance(field, BaseRelationField):
                    name = field.related_name or key
                else:
                    name = field.attname or field.name or key
                result[name] = field.to_simple(value.get(key))

        return result
