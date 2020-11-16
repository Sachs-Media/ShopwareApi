from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.saleschannel import SalesChannelController
from shopwareapi.utils.queryset import Queryset


class SalesChannel(BaseModel):
    """
    model for a shopware SalesChannel

    Attributes:
        FIELDS               tuple of attributes a SalesChannel object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = SalesChannelController

    FIELDS = (
        BaseField("id", "id", aliases=["salesChannelId"], required=False),
        BaseField("name", "name", required=False),
        BaseField("shortname", "shortname", required=False),
        BaseField("vis", "shortname", required=False),
        BaseField("active", "active", required=False),
        BaseField("maintenance", "maintenance", required=False),
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

            model = SalesChannel(options={"client": client()})
            if isinstance(item, SalesChannel):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)
        return key, Queryset(SalesChannel, *result_models)

    @staticmethod
    def convert_product_assignment(queryset, field, local_field, *args, **kwargs):
        result = []
        for item in queryset:
            result.append({"salesChannelId": item.id, "visibility": 30})
        return result
