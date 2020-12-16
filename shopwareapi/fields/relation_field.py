from shopwareapi.core.field import BaseRelationField
import logging

log = logging.getLogger(__name__)


class ForeignKey(BaseRelationField):
    # Single Reference to another Object

    def to_simple(self, val):
        log.debug(self.name)
        log.debug(self.__dict__)
        pk_val = getattr(val, self.related_model._meta.pk.name)
        return val._meta.pk.to_simple(pk_val)


class ManyToOneField(BaseRelationField):
    # List of references to other Objects

    def get_attname(self):
        return self.name

    def from_api(self, *args, **kwargs):
        print(args)
        print(kwargs)