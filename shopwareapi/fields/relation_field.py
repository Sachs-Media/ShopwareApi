from shopwareapi.core.field import BaseField
from shopwareapi.core.field import BaseRelationField


class RelationField(BaseRelationField):
    # Single Reference to another Object

    def get_attname(self):
        return "%sId" % self.model._meta.api_type


class ManyToOneField(BaseRelationField):
    # List of references to other Objects

    def get_attname(self):
        return "%sId" % self.model._meta.api_type
