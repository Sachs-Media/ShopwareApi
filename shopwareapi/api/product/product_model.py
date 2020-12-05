import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    media = fields.ManyToOneField("media.Media")
    manufacturer = fields.ForeignKey("manufacturer.Manufacturer", related_name="manufacturerId")
    unit = fields.ForeignKey("unit.Unit")
    tax = fields.ForeignKey("tax.Tax")
    cover = fields.ForeignKey("product.ProductMedia")
    # - price = fields.VirtualField
    productNumber = fields.CharField()
    stock = fields.IntegerField(null=True)
    restockTime = fields.IntegerField()
    active = fields.BooleanField()
    availableStock = fields.IntegerField(null=True)
    available = fields.BooleanField()
    ean = fields.CharField()
    purchaseSteps = fields.IntegerField(null=True)
    minPurchase = fields.IntegerField(null=True)
    maxPurchase = fields.IntegerField(null=True)
    weight = fields.NumberField(null=True)
    width = fields.NumberField(null=True)
    height = fields.NumberField(null=True)
    length = fields.NumberField(null=True)
    categories = fields.ManyToOneField("category.Category")

    # name
    # description
    # packUnit
    ##- customFields
    # featureSet
    # createdAt
    # updatedAt

    class Meta:
        api_endpoint = "product"
        api_type = "product"
