from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media_folder import MediaFolderController


class MediaFolder(BaseModel):
    CONTROLLER_CLASS = MediaFolderController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("parentId", "parentId", required=False),
        BaseField("configurationId", "configurationId", required=False),
    )

