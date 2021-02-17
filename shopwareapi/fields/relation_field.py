from shopwareapi.core.field import BaseRelationField, return_None
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

    def from_api(self, *args, **kwargs):
        print(args)
        print(kwargs)
        return "bS"

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
            package = {}
            for field in model._meta.fields:
                if field.read_only is False:
                    print("#"*100)
                    print(model)
                    print(field.name)
                    print(getattr(model, field.name))
                    package[field.attname] = field.to_simple(getattr(model, field.name))

            result.append(package)
        return result