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

logging.basicConfig(level=logging.DEBUG)

s = ShopwareClient(
    base_url="http://janao.de",
    version="v3",
    client_id="SWIADTVMAHVTBTY1WJZYD3V2TA",
    client_secret="eWU3MUQyZjJZQXd3ZHNMRjdSYVFhdWRQZ05IUUJxQUlDZ2VEWkk"
)

image = s.controller.Media.find("2001245", matches_field="fileName").all()[0]
print(image.id)
