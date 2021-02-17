import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductCrossSellingModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField()
    position = fields.NumberField(null=True)
    type = fields.CharField() # productList
    active = fields.BooleanField(default=True)
    product = fields.ForeignKey("product.product_model.ProductModel", related_name="productId")
    assignedProducts = fields.ManyToOneField("product.product_cross_selling_assigned_product_model.ProductCrossSellingAssignedProductModel")

    class Meta:
        api_endpoint = "product-cross-selling"
        api_type = "product_cross_selling"
