import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    media = fields.ManyToOneField("media.Media")
    manufacturer = fields.RelationField("manufacturer.Manufacturer", related_name="manufacturerId")
    unit = fields.RelationField("unit.Unit")
    tax = fields.RelationField("tax.Tax")
    cover = fields.RelationField("product.ProductMedia")
    # - price = fields.VirtualField
    productNumber = fields.CharField()
    stock = fields.IntegerField()
    restockTime = fields.IntegerField()
    active = fields.BooleanField()
    availableStock = fields.IntegerField()
    available = fields.BooleanField()
    ean = fields.CharField()
    purchaseSteps = fields.IntegerField()
    minPurchase = fields.IntegerField()
    maxPurchase = fields.IntegerField()
    weight = fields.NumberField()
    width = fields.NumberField()
    height = fields.NumberField()
    length = fields.NumberField()
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
