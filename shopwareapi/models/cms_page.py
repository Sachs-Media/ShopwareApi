from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.cms_page import CmsPageController
from shopwareapi.utils.queryset import Queryset


class CmsPage(BaseModel):
    CONTROLLER_CLASS = CmsPageController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("type", "type", required=False),
    )

    @staticmethod
    def convert_queryset(client, data, field, key):
        result_models = []
        for item in data.get(key):

            model = CmsPage(options={"client": client()})
            if isinstance(item, CmsPage):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(CmsPage, *result_models)
