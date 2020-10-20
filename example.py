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
    base_url="http://janao.de",
    version="v3",
    client_id="SWIADTVMAHVTBTY1WJZYD3V2TA",
    client_secret="eWU3MUQyZjJZQXd3ZHNMRjdSYVFhdWRQZ05IUUJxQUlDZ2VEWkk"
)

coverimage = s.controller.Media.find("2001245", matches_field="fileName").all()[0]
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
    productNumber=1234567,
    stock=99,
    tax=tax,
    manufacturer=manufacturer,
    price=[price],
    ean="123456",
    packUnit="stk",
    purchaseUnit=1,
    description="asdf",
    media=Queryset(Media, Media(
        **{
            "id": linkimageid,
            "mediaId": coverimage.id,
            "position": 0,
        }
    )),
    coverId=linkimageid,
    options={"client": s}
)# .controller.create(options={"identifierName": "productNumber"})

print(json.dumps(product_creation.get_dict(), cls=ComplexEncoder))
print("#"*20)
print(product_creation.__dict__)
product_creation.controller.create(options={"identifierName": "productNumber"})
