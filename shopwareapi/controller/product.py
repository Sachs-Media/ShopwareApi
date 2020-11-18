from shopwareapi.core.basecontroller import BaseController
from shopwareapi.models.media_relation import MediaRelation
from shopwareapi.utils.queryset import Queryset


class ProductController(BaseController):
    """
    controller class for a shopware product

    Attributes:
        api_model     Name of the Api model or endpoint model name.
    """
    api_model = "product"

    def get_product_media(self):
        request_url = self.get_client().build_url(model="product/{}/media".format(self.model.id))
        result = self.get_client().get(request_url)
        result_list = []

        for item in result.get("data"):

            result_list.append(self.get_client().controller.MediaRelation.get(item.get("id")))

        return Queryset(MediaRelation, *result_list)
