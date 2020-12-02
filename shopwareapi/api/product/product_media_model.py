from shopwareapi import fields
from shopwareapi.api.media.media_model import MediaModel
from shopwareapi.core.model import Model


class ProductMediaModel(Model):
    id = fields.UUIDField(aliases=("productId"))
    media = fields.ForeignKey("media.Media")

    class Meta:
        api_endpoint = "product"
