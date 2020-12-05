import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductMediaModel(Model):
    id = fields.UUIDField(aliases=("productId"), default=uuid.uuid4)
    media = fields.ForeignKey("media.Media")

    class Meta:
        api_endpoint = "product"
