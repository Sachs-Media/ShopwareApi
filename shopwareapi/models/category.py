from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.category import CategoryController


class Category(BaseModel):

    CONTROLLER_CLASS = CategoryController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("description", "description", required=False),
        BaseField("parentId", "parentId", required=False),
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
