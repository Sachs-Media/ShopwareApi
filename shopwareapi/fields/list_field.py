from shopwareapi.core.field import BaseField, BaseRelationField
import json
from shopwareapi.core.model import Model
import logging

log = logging.getLogger(__name__)


class ListField(BaseField):

    def __init__(self, verbose_name=None, schema=None, **kwargs):
        if schema is None:
            raise AttributeError("Please define a Schema")
        self._schema = schema

        super().__init__(verbose_name, **kwargs)

    def get_internal_type(self):
        return "ListField"

    def to_python(self, value):
        return value

    def to_simple(self, value):
        result = []

        for item in value:
            result.append(self._schema.to_simple(item))
        return result