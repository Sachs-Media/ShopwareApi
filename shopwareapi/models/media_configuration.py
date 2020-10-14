from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media_configuration import MediaConfigurationController


class MediaConfiguration(BaseModel):
    CONTROLLER_CLASS = MediaConfigurationController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("type", "type", required=False),
    )

