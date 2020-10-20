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
import requests
import io
import json
import os

logging.basicConfig(level=logging.DEBUG)

s = ShopwareClient(
    base_url="http://janao.de",
    version="v3",
    client_id="SWIADTVMAHVTBTY1WJZYD3V2TA",
    client_secret="eWU3MUQyZjJZQXd3ZHNMRjdSYVFhdWRQZ05IUUJxQUlDZ2VEWkk"
)

endpoint = "http://janao.de/api/v3/"
payload = {}

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer {token}".format(token=s._get_token())
}

