from shopwareapi.core.model import Model
from shopwareapi import fields
from shopwareapi.api.product.product_media_model import MediaModel


class ProductModel(Model):
    id = fields.UUIDField(aliases=("productId"))
    media = fields.ForeignKey(MediaModel)

    class Meta:
        api_model = "product"