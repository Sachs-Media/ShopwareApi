import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class CategoryModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    parent = fields.CharField()#fields.ForeignKey("self", null=True)
    name = fields.CharField(max_length=255)

    class Meta:
        api_endpoint = "category"
        api_type = "category"
