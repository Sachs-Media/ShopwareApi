from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.media_relation import MediaRelationController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert
from shopwareapi.models.media import Media
from shopwareapi.models.custom_field import CustomField


class MediaRelation(BaseModel):
    CONTROLLER_CLASS = MediaRelationController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("mediaId", "mediaId", converter=Media.convert, related_to="media"),
        BaseField("media", "media", required=False, nested=True, converter=Media.convert),
        BaseField("position", "position", required=True, converter=Convert.to_int),
        BaseField("productId", "productId", required=False),
    )

    @staticmethod
    def convert_queryset(client, data, field, key):
        result_models = []
        for item in data.get(key):

            model = MediaRelation(options={"client": client()})
            if isinstance(item, MediaRelation):
                result_models.append(item)
            elif item is not None:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(MediaRelation, *result_models)