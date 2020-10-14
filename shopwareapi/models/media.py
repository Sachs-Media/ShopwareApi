from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media import MediaController


class Media(BaseModel):
    CONTROLLER_CLASS = MediaController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("mediaFolderId", "mediaFolderId", required=False),
        BaseField("fileName", "fileName", required=False),
        BaseField("fileExtension", "fileExtension", required=False),
    )

