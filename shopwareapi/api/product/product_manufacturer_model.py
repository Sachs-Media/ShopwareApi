import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductManufacturerModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField()
    media = fields.ForeignKey("media.media_model.MediaModel", related_name="mediaId")

    class Meta:
        api_endpoint = "product-manufacturer"
        api_type = "product_manufacturer"
