from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.price import PriceController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert
from shopwareapi.models.currency import Currency


class Price(BaseModel):
    """
    model for a shopware Price

    Attributes:
        FIELDS               tuple of attributes a Price object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PriceController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("netPrice", "net", required=False, converter=Convert.to_float),
        BaseField("grossPrice", "gross", required=False, converter=Convert.to_float),
        BaseField("totalPrice", "totalPrice", required=False),
        BaseField("linked", "linked", required=False, converter=Convert.to_boolean),
        BaseField("positionPrice", "positionPrice", required=False),
        BaseField("taxStatus", "taxStatus", required=False),
        BaseField("listPrice", "listPrice", required=False),
        BaseField("price", "price", required=False),
        BaseField("discount", "discount", required=False),
        BaseField("percentage", "percentage", required=False),
        BaseField("currency", "currency", required=False, converter=Currency.convert, nested=True),
        BaseField("currencyId", "currencyId", converter=Currency.convert, related_to="currency"),
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
            
            model = Price(options={"client": client()})
            if isinstance(item, Price):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)
    
        return key, Queryset(Price, *result_models)

