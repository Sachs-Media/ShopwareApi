from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.category import CategoryController
from shopwareapi.utils.queryset import Queryset


class Category(BaseModel):

    CONTROLLER_CLASS = CategoryController

    @staticmethod
    def convert(client, data, field, key):
        category = data.get(key)

        if isinstance(category, Category):
            return "category", category
        elif key == "parentId":
            model = client().controller.Category.get(category)
            return "category", model

    FIELDS = (
        BaseField("id", "id", aliases=["parentId"], required=False),
        BaseField("parentId", "parentId", required=False, converter=convert),
        BaseField("name", "name", required=False),
        BaseField("description", "description", required=False),
        BaseField("afterCategoryId", "afterCategoryId", required=False),
        BaseField("mediaId", "mediaId", required=False),
        BaseField("breadcrumb", "breadcrumb", required=False),
        BaseField("level", "level", required=False),
        BaseField("path", "path", required=False),
        BaseField("active", "active", required=False),
        BaseField("customFields", "customFields", required=False),
        BaseField("metaTitle", "metaTitle", required=False),
        BaseField("metaDescription", "metaDescription", required=False),
        BaseField("keywords", "keywords", required=False),
        BaseField("products", "products", required=False),
        BaseField("productStream", "productStream", required=False),
        BaseField("navigationSalesChannels", "navigationSalesChannels", required=False),
        BaseField("footerSalesChannels", "footerSalesChannels", required=False),
        BaseField("serviceSalesChannels", "serviceSalesChannels", required=False),
    )


    @staticmethod
    def convert_queryset(client, data, field, key):
        result_models = []
        for item in data.get(key):

            model = Category(options={"client": client()})
            if isinstance(item, Category):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)
        return key, Queryset(Category, *result_models)
