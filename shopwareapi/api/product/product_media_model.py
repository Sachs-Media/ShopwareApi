import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductMediaModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    product = fields.ForeignKey("product.product_model.ProductModel", related_name="productId")
    media = fields.ForeignKey("media.media_model.MediaModel", related_name="mediaId")

    class Meta:
        api_endpoint = "product-media"
        api_type = "product_media"
