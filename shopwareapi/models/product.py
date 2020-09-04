from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.utils.converter import Convert
from shopwareapi.controller.product import ProductController
from shopwareapi.models.price import Price


class Product(BaseModel):
  
  CONTROLLER_CLASS = ProductController
  
  FIELDS = (
    BaseField("id", "id", required=False),
    BaseField("uuid", "uuid", required=False),
    BaseField("uidtId", "uidtId", required=False),
    BaseField("taxId", "taxId", required=False),
    BaseField("price", "price", required=False, converter=Price.convert_queryset, nested=True),
    BaseField("productNumber", "productNumber", required=False),
    BaseField("stock", "stock", required=False, converter=Convert.to_int),
    BaseField("active", "active", required=False, converter=Convert.to_boolean),
    BaseField("ean", "ean", required=False),
    BaseField("weight", "weight", required=False),
    BaseField("width", "width", required=False),
    BaseField("height", "height", required=False),
    BaseField("length", "length", required=False),
    BaseField("categoryTree", "categoryTree", required=False),
    BaseField("name", "name", required=False),
    BaseField("keywords", "keywords", required=False),
    BaseField("packUnit", "packUnit", required=False),
    BaseField("packUnitPlural", "packUnitPlural", required=False),
    BaseField("featureSet", "featureSet", required=False),
    BaseField("markAsTopseller", "markAsTopseller", required=False),
    BaseField("mainCategories", "mainCategories", required=False),
    BaseField("tags", "tags", required=False),
    BaseField("tax", "tax", required=False),
    BaseField("description", "description", required=False),
    BaseField("customFields", "customFields", required=False),
    BaseField("crossSelling", "crossSelling", required=False),
    BaseField("manufacturer", "manufacturer", required=False),
    BaseField("unit", "unit", required=False),
    BaseField("media", "media", required=False),
    BaseField("visibilities", "visibilities", required=False)
  )
