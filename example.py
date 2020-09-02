from shopwareapi.client import ShopwareClient
from shopwareapi.models.product import Product



s = ShopwareClient(base_url="http://localhost:8000", version="v3", client_id="SWIAVUDPDJNQR2W4SULHODZ4AW", client_secret="bUh5ZkxEaUtYOEVQa0JaaXJxVE92S09BTmVaY1RsOEF5clA5dDQ")


# s.controller.Currency.find(term="EUR")

#result_list = s.controller.Product.find(term="light")


#a = result_list.all()

#print([item.price for item in result_list.all()])


# p = Product(name="marvin", productNumber="1337", stock=10, taxId="03f165404f214c53ab95301965887cc9", options={"client": s})
# r = p.controller.create(price = [
#     {
#         "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
#         "gross": 150000,
#         "net": 10,
#         "linked": False
#     }

# ])

# print(r)






# url = s.build_url(model="_action/sync")

# s.post(url, 
#         data={
#             "write-product": {
#                 "entity": "product",
#                 "action": "upsert",
#                 "payload": [
#                     {
#                         "name": "marvin asdf",
#                         "productNumber": "1337",
#                         "stock": 10,
#                         "taxId": "03f165404f214c53ab95301965887cc9",
#                         "price": [
#                             {
#                                 "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
#                                 "gross": 150000,
#                                 "net": 10,
#                                 "linked": False
#                             }
#                         ]
#                     }
#                 ]
#             }
#         }
#         )