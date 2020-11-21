from shopwareapi.core.model import Model
from shopwareapi import fields


class MediaModel(Model):
    id = fields.UUIDField(aliases=("productId"))

    class Meta:
        api_model = "media"