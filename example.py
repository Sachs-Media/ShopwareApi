from shopwareapi.client import ShopwareClient
from shopwareapi.models import CustomFieldSetRelation, CustomField
from shopwareapi.utils.queryset import Queryset

c = ShopwareClient("https://www.janao.de", "v3", "SWIAZ0G2RTBYELHIMEZHQMXXAQ", "VzlzNjU0OWh3VGNucUs0RXpOY05YU1d2dUFUTHJ6YVRRVUVqRlg")


folder = c.controller.MediaFolder.get("478f2ccf493e4f95a37b97834535d974")

folder_content = folder.controller.find("2005361_H", related_name="media")

media = folder_content.first()
print(media.customFields)
media.customFields = {"foobar_test":"azerzsezerzserz"}
print(media.controller.update())