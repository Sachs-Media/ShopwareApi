from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.utils.converter import Convert
from shopwareapi.controller.product import ProductController
from shopwareapi.models.price import Price
from shopwareapi.models.tax import Tax
from shopwareapi.models.manufacturer import Manufacturer
from shopwareapi.models.media_relation import MediaRelation
from shopwareapi.models.category import Category
from shopwareapi.models.saleschannel import SalesChannel


class Product(BaseModel):
    """
    model for a shopware Product

    Attributes:
        FIELDS               tuple of attributes a Product object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = ProductController
    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("coverId", "coverId", required=False),
        BaseField("media", "media",
                  required=False,
                  converter=MediaRelation.convert_queryset,
                  related_to="self",
                  nested=True),
        BaseField("categories", "categories",
                  required=False,
                  converter=Category.convert_queryset,
                  related_to="self",
                  nested=True,
                  secondary_converter=Category.convert_only_from_queryset("id")),
        BaseField("visibilities", "visibilities",
                  required=False,
                  converter=SalesChannel.convert_queryset,
                  related_to="self",
                  nested=True,
                  secondary_converter=SalesChannel.convert_product_assignment),
        BaseField("price", "price", required=False, converter=Price.convert_queryset, related_to="self", nested=True),
        BaseField("uuid", "uuid", required=False),
        BaseField("uidtId", "uidtId", required=False),
        BaseField("tax", "tax", required=False, nested=True, converter=Tax.convert),
        BaseField("taxId", "taxId", converter=Tax.convert, related_to="tax"),
        BaseField("manufacturer", "manufacturer", required=False, nested=True, converter=Manufacturer.convert),
        BaseField("manufacturerId", "manufacturerId", converter=Manufacturer.convert, related_to="manufacturer"),
        BaseField("productNumber", "productNumber", required=False),
        BaseField("stock", "stock", required=False, converter=Convert.to_int),
        BaseField("active", "active", required=False, converter=Convert.to_boolean),
        BaseField("ean", "ean", required=False),
        BaseField("weight", "weight", required=False),
        BaseField("width", "width", required=False),
        BaseField("height", "height", required=False),
        BaseField("length", "length", required=False),
        BaseField("categoryTree", "categoryTree", required=False, read_only=True),
        BaseField("name", "name", required=False),
        BaseField("keywords", "keywords", required=False),
        BaseField("packUnit", "packUnit", required=False),
        BaseField("packUnitPlural", "packUnitPlural", required=False),
        BaseField("featureSet", "featureSet", required=False),
        BaseField("markAsTopseller", "markAsTopseller", required=False),
        BaseField("mainCategories", "mainCategories", required=False),
        BaseField("tags", "tags", required=False),
        BaseField("description", "description", required=False),
        BaseField("customFields", "customFields", required=False, converter=Convert.to_dict),
        BaseField("crossSelling", "crossSelling", required=False),
        BaseField("unit", "unit", required=False),
    )

