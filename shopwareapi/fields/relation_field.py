from shopwareapi.core.field import BaseRelationField, return_None, BaseField
from shopwareapi.core.lazymodel import LazyModel
from shopwareapi.core.query import QuerySet
import logging

log = logging.getLogger(__name__)


class ForeignKey(BaseRelationField):
    # Single Reference to another Object

    def to_simple(self, val):
        if isinstance(val, LazyModel):
            return val._kwargs[val._model._meta.pk.name]
        pk_val = getattr(val, self.related_model._meta.pk.name)
        return val._meta.pk.to_simple(pk_val)


class ManyToOneField(BaseRelationField):
    # List of references to other Objects

    def get_attname(self):
        return self.name

    def _get_default(self):
        res = super(ManyToOneField, self)._get_default()
        if res is not None and res is not str:
            return res

        def wrapper():
            return QuerySet(self.get_related_model_class())
        return wrapper

    def to_simple(self, val):
        result = []

        for model in val:
            if type(model) is dict:
                package = {}
                for key, value in model.items():
                    for field in self.get_related_model_class()._meta.fields:
                        if key == field.attname or key == field.name:
                            if isinstance(field, BaseField):
                                package[field.get_attname()] = field.to_simple(value)
                            else:
                                package[field.get_attname()] = value._get_pk_val()
                result.append(package)
            else:
                package = {}
                for field in model._meta.fields:
                    if field.read_only is False:
                        if getattr(model, field.name):
                            package[field.get_attname()] = field.to_simple(getattr(model, field.name))
                result.append(package)
        return result