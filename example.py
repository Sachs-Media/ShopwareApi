from shopwareapi.client import ShopwareClient
from shopwareapi.models.price import Price
from shopwareapi.models.product import Product
from shopwareapi.models.manufacturer import Manufacturer
import sys
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

s = ShopwareClient(
    base_url="http://janao.de",
    version="v3",
    client_id="SWIADTVMAHVTBTY1WJZYD3V2TA",
    client_secret="eWU3MUQyZjJZQXd3ZHNMRjdSYVFhdWRQZ05IUUJxQUlDZ2VEWkk"
)

cur = s.controller.Currency.find("EUR").all()[0]
tax = s.controller.Tax.find(19.0, matches_field="taxRate").all()[0]

price = Price(** {
             "currency": cur,
             "gross": 150000,
             "net": 10,
             "linked": False,
             "options": {"client": s}
         }
)

Manufacturer(
    name="Aircraft",
    options={"client": s}
).controller.get_or_create(options={"identifierName": "name"})

test_manufacturer = s.controller.Manufacturer.find("Aircraft", matches_field="name").all()[0]

create_product = Product(
    name="asdfsdfadfdfgsgfhsghfgfgffgd",
    productNumber="89fe4b60-a9e5-455e-b2cc-8d8f6cacbca3",
    manufacturer=test_manufacturer,
    stock=10,
    tax=tax,
    price=[price],
    options={"client": s}
).controller.get_or_create(options={"identifierName": "productNumber"})
