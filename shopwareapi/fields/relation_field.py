from shopwareapi.core.field import BaseField
from shopwareapi.core.field import BaseRelationField


class ForeignKey(BaseRelationField):
    # Single Reference to another Object

    def to_simple(self, val):
        pk_val = getattr(val, self.related_model._meta.pk.name)
        return val._meta.pk.to_simple(pk_val)


class ManyToOneField(BaseRelationField):
    # List of references to other Objects

    def get_attname(self):
        return "%sId" % self.name
