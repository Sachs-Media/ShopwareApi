from shopwareapi.client import ShopwareClient
from shopwareapi.models.price import Price
from shopwareapi.models.product import Product
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
#find  = s.controller.Product.find(term="light")
#get   = s.controller.Product.get(term="aa019a7fef714322a863c3572cc566bb")
#patch = s.controller.Product.patch(uuid="aa019a7fef714322a863c3572cc566bb")

cur = s.controller.Currency.find("EUR").all()[0]
tax = s.controller.Tax.find(19.0, matches_field="taxRate").all()[0]

print(tax)

price = Price(** {
             "currency": cur,
             "gross": 150000,
             "net": 10,
             "linked": False,
             "options": {"client": s}
         }
)

create_product = Product(
    name="asdfsdfadfdfgsgfhsghfgfgffgd",
    productNumber=uuid.uuid4(),
    stock=10,
    tax=tax,
    price=[price],
    options={"client": s}
).controller.create()

create_product.name="es hat funktioniert"
create_product.controller.update()
