from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media import MediaController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert


class Media(BaseModel):
    """
    model for a shopware Media

    Attributes:
        FIELDS               tuple of attributes a Media object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = MediaController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("mediaId", "mediaId", required=False),
        BaseField("mediaFolderId", "mediaFolderId", required=False),
        BaseField("fileName", "fileName", required=False),
        BaseField("fileExtension", "fileExtension", required=False),
        BaseField("position", "position", converter=Convert.to_int, required=False),
    )

    @staticmethod
    def convert_queryset(client, data, field, key):
        """
        converts the data to a queryset

        Parameters:
        client:             client object to connect with a shopware api
        data:               dictionary

        Returns:
        key, Queryset object

       """
        result_models = []
        for item in data.get(key):

            model = Media(options={"client": client()})
            if isinstance(item, Media):
                result_models.append(item)
            elif item is not None:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(Media, *result_models)

    @staticmethod
    def convert_product_assignment(queryset, field, local_field, *args, **kwargs):
        result = []
        for item in queryset:
            a = {"position": item.position}
            if hasattr(item, "mediaId"):
                a.update({"mediaId": item.mediaId})
            elif hasattr(item, "id"):
                a.update({"id":item.id})
            else:
                raise ValueError("Missing Identifier for Media Object")
            result.append(a)
        return result
