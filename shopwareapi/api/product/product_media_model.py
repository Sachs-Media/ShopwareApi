from shopwareapi.core.model import Model
from shopwareapi import fields
from shopwareapi.api.media.media_model import MediaModel


class ProductMediaModel(Model):
    id = fields.UUIDField(aliases=("productId"))
    media = fields.RelationField(MediaModel)

    class Meta:
        api_endpoint = "product"