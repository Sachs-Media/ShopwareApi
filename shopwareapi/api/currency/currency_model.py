import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class CurrencyModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    isoCode = fields.CharField(max_length=255)
    shortName = fields.CharField(max_length=255)

    class Meta:
        api_endpoint = "currency"
        api_type = "currency"
