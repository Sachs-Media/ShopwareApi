import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField()
    manufacturer = fields.ForeignKey("product.product_manufacturer_model.ProductManufacturerModel", related_name="manufacturerId")
    unit = fields.ForeignKey("unit.Unit")
    tax = fields.ForeignKey("tax.tax_model.TaxModel", related_name="taxId")
    cover = fields.ForeignKey("product.product_media_model.ProductMediaModel", related_name="coverId", null=True)
    price = fields.ListField(schema=fields.DictField(schema={
        "gross": fields.NumberField(),
        "net": fields.NumberField(),
        "currency": fields.ForeignKey("currency.currency_model.CurrencyModel", related_name="currencyId"),
        "linked": fields.BooleanField(default=False)
    }))
    visibilities = fields.ListField(schema=fields.DictField(schema={
        "salesChannel": fields.ForeignKey("sales_channel.sales_channel_model.SalesChannelModel", related_name="salesChannelId"),
        "visibility": fields.NumberField(),
    }))
    productNumber = fields.CharField()
    stock = fields.IntegerField(null=True)
    restockTime = fields.IntegerField(null=True)
    active = fields.BooleanField(default=True)
    availableStock = fields.IntegerField(null=True)
    available = fields.BooleanField(default=True)
    ean = fields.CharField()
    purchaseSteps = fields.IntegerField(null=True)
    minPurchase = fields.IntegerField(null=True)
    maxPurchase = fields.IntegerField(null=True)
    weight = fields.NumberField(null=True)
    width = fields.NumberField(null=True)
    height = fields.NumberField(null=True)
    length = fields.NumberField(null=True)
    categoryTree = fields.ManyToOneField("category.category_model.CategoryModel")

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
