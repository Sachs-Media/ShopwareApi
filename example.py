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
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)

s = ShopwareClient(
  base_url="http://janao.de",
  version="v3",
  client_id="SWIADTVMAHVTBTY1WJZYD3V2TA",
  client_secret="eWU3MUQyZjJZQXd3ZHNMRjdSYVFhdWRQZ05IUUJxQUlDZ2VEWkk"
)

# Media(
#   **{
#     "options": {"client": s}
#   }
# ).controller.create(options={"identifierName": "name"})


# cur = s.controller.Currency.find("EUR").all()[0]
# tax = s.controller.Tax.find(19.0, matches_field="taxRate").all()[0]
# sf = s.controller.SalesChannel.find("Storefront", matches_field="name").all()[0]
# hs = s.controller.SalesChannel.find("Headless", matches_field="name").all()[0]

# product_folder = s.controller.MediaFolder.find("Product Media", matches_field="name").all()[0]
# media_configuration = s.controller.MediaConfiguration.find(True, matches_field="createThumbnails").all()[0]
#
# mediafolder = MediaFolder(**{
#   "name": "földer_öne",
#   "configurationId": media_configuration.id,
#   "parentId": product_folder.id,
#   "options": {"client": s}
# }).controller.create(options={"identifierName": "name"})

#
# price = Price(**{
#   "currency": cur,
#   "gross": 150000,
#   "net": 10,
#   "linked": False,
#   "options": {"client": s}
# })
#
# Manufacturer(
#   name="Aircraft",
#   options={"client": s}
# ).controller.get_or_create(options={"identifierName": "name"})
#
# test_manufacturer = s.controller.Manufacturer.find("Aircraft", matches_field="name").all()[0]
# saleschannels = Queryset(SalesChannel, *[sf, hs])
#
# create_product = Product(
#   name="asdfsdfadfdfgsgfhsghfgfgffgd",
#   productNumber="89fe4b60-a9e5-455e-b2cc-8d8f6cacbca3",
#   manufacturer=test_manufacturer,
#   categories="",
#   stock=10,
#   tax=tax,
#   price=[price],
#   options={"client": s},
#   visibilities=saleschannels
# ).controller.get_or_create(options={"identifierName": "productNumber"})
