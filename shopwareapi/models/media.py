from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media import MediaController
from shopwareapi.utils.queryset import Queryset


class Media(BaseModel):
    CONTROLLER_CLASS = MediaController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("mediaFolderId", "mediaFolderId", required=False),
        BaseField("fileName", "fileName", required=False),
        BaseField("fileExtension", "fileExtension", required=False),
    )

    @staticmethod
    def convert_queryset(client, data, field, key):
        result_models = []
        for item in data.get(key):

            model = Media(options={"client": client()})
            if isinstance(item, Media):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(Media, *result_models)
