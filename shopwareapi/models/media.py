from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media import MediaController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert
from shopwareapi.models.custom_field import CustomField


class Media(BaseModel):
    """
    model for a shopware Media

    Attributes:
        FIELDS               tuple of attributes a Media object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = MediaController

    FIELDS = (
        BaseField("id", "id", aliases=["mediaId"], required=False),
        BaseField("mediaFolderId", "mediaFolderId", required=False),
        BaseField("fileName", "fileName", read_only=True, required=False),
        BaseField("fileExtension", "fileExtension", read_only=True, required=False),
        BaseField("customFields", "customFields", converter=Convert.to_dict, required=False),
        BaseField("hasFile", "hasFile", read_only=True, converter=Convert.to_boolean, required=False),
        BaseField("position", "position", converter=Convert.to_int, required=False),
        BaseField("translations", "translations", read_only=True),
    )

    @staticmethod
    def convert(client, data, field, key):
        media = data.get(key)

        if isinstance(media, Media):
            return "media", media
        elif key == "mediaId":
            model = client().controller.Media.get(media)
            return "media", model
        return key, media