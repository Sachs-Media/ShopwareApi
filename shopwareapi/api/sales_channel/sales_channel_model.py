import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class SalesChannelModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)



    class Meta:
        api_endpoint = "sales-channel"
        api_type = "sales_channel"
