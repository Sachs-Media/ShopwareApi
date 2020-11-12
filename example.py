from shopwareapi.client import ShopwareClient
from shopwareapi.models.price import Price
from shopwareapi.models.product import Product
from shopwareapi.models.manufacturer import Manufacturer
from shopwareapi.utils.queryset import Queryset
from shopwareapi.models.category import Category
from shopwareapi.models.saleschannel import SalesChannel
from shopwareapi.models.cms_page import CmsPage
from shopwareapi.models.media_folder import MediaFolder
from shopwareapi.models.media_configuration import MediaConfiguration
from shopwareapi.models.media import Media
from shopwareapi.utils.json_hook import ComplexEncoder
import logging
import uuid
import json


logging.basicConfig(level=logging.DEBUG)

s = ShopwareClient(
    base_url="http://195.201.135.86",
    version="v2",
    client_id="SWIAA3Q0A0JMCWLZQZYWBHRTWQ",
    client_secret="czRrMm1rbXJpMllKeWd0ZVBHRDl0cHJUT2I4NEVkck9pSVRJVGQ"
)

manufacturer = s.controller.Manufacturer.find("Aircraft", matches_field="name").all()[0]

cur = s.controller.Currency.find("EUR").all()[0]

tax = s.controller.Tax.find(19.0, matches_field="taxRate").all()[0]

price = Price(
    **{
        "currency": cur,
        "gross": 1555,
        "net": 1212,
        "linked": False,
        "options": {"client": s}
    }
)

linkimageid = uuid.uuid4().hex

product_creation = Product(
    name="blubbl",
    productNumber="123455655",
    stock=99,
    tax=tax,
    manufacturer=manufacturer,
    price=[price],
    ean="123456",
    packUnit="stk",
    purchaseUnit=1,
    description="asdf",
    options={"client": s}
).controller.get_or_create(options={"identifierName": "productNumber"})

print(product_creation.get_dict())
