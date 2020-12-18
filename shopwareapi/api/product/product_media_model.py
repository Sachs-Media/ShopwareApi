import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductMediaModel(Model):
    id = fields.UUIDField(primary_key=True, aliases=("coverId",), default=uuid.uuid4)
    product = fields.ForeignKey("product.product_model.ProductModel", related_name="productId", null=True)
    position = fields.NumberField(null=True)
    media = fields.ForeignKey("media.media_model.MediaModel", related_name="mediaId")

    class Meta:
        api_endpoint = "product-media"
        api_type = "product_media"
