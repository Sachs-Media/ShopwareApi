from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media_configuration import MediaConfigurationController


class MediaConfiguration(BaseModel):
    """
    model for a shopware MediaConfiguration

    Attributes:
        FIELDS               tuple of attributes a MediaConfiguration object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = MediaConfigurationController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("type", "type", required=False),
        BaseField("createThumbnails", "createThumbnails", required=False),
        BaseField("keepAspectRatio", "keepAspectRatio", required=False),
        BaseField("thumbnailQuality", "thumbnailQuality", required=False),
        BaseField("private", "private", required=False),
        BaseField("noAssociation", "noAssociation", required=False),
        BaseField("customFields", "customFields", required=False)
    )

