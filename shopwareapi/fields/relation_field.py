from shopwareapi.core.field import BaseField


class RelationObject:
    pass

class RelationField(BaseField, RelationObject):

    def __init__(self, relation, **kwargs):
        self.releation = relation
        super().__init__(**kwargs)

    def get_attname(self):
        return "%sId" % self.model._meta.api_type