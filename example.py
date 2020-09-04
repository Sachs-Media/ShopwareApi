from shopwareapi.client import ShopwareClient
from shopwareapi.models.price import Price
from shopwareapi.models.product import Product
import sys
import uuid
s = ShopwareClient(
    base_url="http://localhost:8000",
    version="v3",
    client_id="SWIAVUDPDJNQR2W4SULHODZ4AW",
    client_secret="bUh5ZkxEaUtYOEVQa0JaaXJxVE92S09BTmVaY1RsOEF5clA5dDQ"
)

# aa019a7fef714322a863c3572cc566bb

#find = s.controller.Product.find(term="light")
#get = s.controller.Product.get(term="aa019a7fef714322a863c3572cc566bb")
#patch = s.controller.Product.patch(uuid="aa019a7fef714322a863c3572cc566bb")
cur = s.controller.Currency.find("EUR").all()[0]
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
    taxId="03f165404f214c53ab95301965887cc9",
    price=[price],
    options={"client": s}
).controller.create()
create_product.name="es hat funktioniert"
create_product.controller.update()
