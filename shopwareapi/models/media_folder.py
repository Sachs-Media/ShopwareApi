from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media_folder import MediaFolderController


class MediaFolder(BaseModel):
    """
    model for a shopware MediaFolder

    Attributes:
        FIELDS               tuple of attributes a MediaFolder object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = MediaFolderController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("parentId", "parentId", required=False),
        BaseField("configurationId", "configurationId", required=False),
    )

