from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.category import CategoryController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert


class Category(BaseModel):
    """
    model for a shopware Category

    Attributes:
        FIELDS               tuple of attributes a Category object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = CategoryController

    FIELDS = (
        BaseField("id", "id", aliases=["categoryId"], required=False),
        BaseField("parentId", "parentId", required=False),
        BaseField("categoryId", "categoryId", related_to="parentId"),
        BaseField("name", "name", required=False),
        BaseField("description", "description", required=False),
        BaseField("afterCategoryId", "afterCategoryId", required=False),
        BaseField("mediaId", "mediaId", required=False),
        BaseField("breadcrumb", "breadcrumb", required=False, read_only=True),
        BaseField("level", "level", required=False, converter=Convert.to_int),
        BaseField("cmsPageId", "cmsPageId", required=False),
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
        BaseField("active", "active", required=False, converter=Convert.to_boolean),
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
            model = Category(options={"client": client()})

            if isinstance(item, Category):
                result_models.append(item)

            else:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(Category, *result_models)
