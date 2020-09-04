from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.saleschannel import SalesChannelController


class SalesChannel(BaseModel):
    CONTROLLER_CLASS = SalesChannelController

    FIELDS = (
        BaseField("name", "name", required=False),
        BaseField("shortname", "shortname", required=False),
        BaseField("active", "active", required=False),
        BaseField("maintenance", "maintenance", required=False),
    )