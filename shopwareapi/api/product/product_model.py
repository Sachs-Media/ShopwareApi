import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class ProductPrice(Model):
    gross = fields.NumberField()
    net = fields.NumberField()
    currency = fields.ForeignKey("currency.currency_model.CurrencyModel", related_name="currencyId")
    linked = fields.BooleanField(default=False)


class ProductModel(Model):
    id = fields.UUIDField(primary_key=True, aliases=("productId", ), default=uuid.uuid4)
    name = fields.CharField()
    description = fields.CharField()
    manufacturer = fields.ForeignKey("product.product_manufacturer_model.ProductManufacturerModel", related_name="manufacturerId")
    unit = fields.ForeignKey("unit.Unit")
    tax = fields.ForeignKey("tax.tax_model.TaxModel", related_name="taxId")
    cover = fields.ForeignKey("product.product_media_model.ProductMediaModel", related_name="coverId")

    price = fields.ManyToOneField(ProductPrice)

    visibilities = fields.ListField(schema=fields.DictField(schema={
        "salesChannel": fields.ForeignKey("sales_channel.sales_channel_model.SalesChannelModel", related_name="salesChannelId"),
        "visibility": fields.NumberField(),
    }))

    media = fields.ManyToOneField("product.product_media_model.ProductMediaModel")

    #media = fields.ListField(schema=fields.DictField(schema={
    #    "id": fields.ForeignKey("product.product_media_model.ProductMediaModel", related_name="id"),
    #    "mediaId": fields.ForeignKey("media.media_model.MediaModel", related_name="mediaId"),
    #    "position": fields.NumberField()
    #}))

    categories = fields.ListField(schema=fields.DictField(schema={
        "id": fields.ForeignKey("category.category_model.CategoryModel", related_name="id")
    }))
    tags = fields.ListField(schema=fields.DictField(schema={
        "id": fields.ForeignKey("tag.tag_model.TagModel", related_name="id")
    }))
    productNumber = fields.CharField()
    stock = fields.IntegerField(null=True)
    restockTime = fields.IntegerField(null=True)
    active = fields.BooleanField(default=True)
    ean = fields.CharField()
    purchaseUnit = fields.CharField(null=True)
    packUnit = fields.CharField(null=True)
    purchaseSteps = fields.IntegerField(null=True)
    minPurchase = fields.IntegerField(null=True)
    maxPurchase = fields.IntegerField(null=True)
    weight = fields.NumberField(null=True)
    width = fields.NumberField(null=True)
    height = fields.NumberField(null=True)
    length = fields.NumberField(null=True)
    categoryTree = fields.ListField(schema=fields.CharField(null=False), read_only=True)


    #categoryTree = fields.ManyToOneField("category.category_model.CategoryModel")
    #crossSellings = fields.ListField(schema=fields.ForeignKey("product.product_cross_selling_model.ProductCrossSellingModel"))
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
