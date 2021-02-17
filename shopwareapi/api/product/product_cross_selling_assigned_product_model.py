import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductCrossSellingAssignedProductModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    product = fields.ForeignKey("product.product_model.ProductModel", related_name="productId")
    #position = fields.NumberField(null=True)

    class Meta:
        api_endpoint = "product-cross-selling-assigned-products"
        api_type = "product_cross_selling_assigned_products"
