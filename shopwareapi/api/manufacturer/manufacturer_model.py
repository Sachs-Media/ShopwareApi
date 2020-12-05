import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ManufacturerModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        api_endpoint = "manufacturer"
        api_type = "manufacturer"