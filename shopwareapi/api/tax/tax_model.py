import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class TaxModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    taxRate = fields.NumberField(null=True)
    name = fields.CharField(null=True)

    class Meta:
        api_endpoint = "tax"
        api_type = "tax"