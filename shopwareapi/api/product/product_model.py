from shopwareapi.core.model import Model
from shopwareapi import fields
from shopwareapi.api.product.product_media_model import MediaModel
import uuid


class ProductModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    media = fields.RelationField(MediaModel)

    class Meta:
        api_endpoint = "product"
        api_type = "product"