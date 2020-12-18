import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class TagModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(null=True)

    class Meta:
        api_endpoint = "tag"
        api_type = "tag"