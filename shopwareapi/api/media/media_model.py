from shopwareapi import fields
from shopwareapi.core.model import Model


class MediaModel(Model):
    id = fields.UUIDField(aliases=("productId"))

    class Meta:
        api_endpoint = "media"
