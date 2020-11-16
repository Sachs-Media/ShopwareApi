from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.currency import CurrencyController
from shopwareapi.utils.converter import Convert


class Currency(BaseModel):
    """
    model for a shopware Currency

    Attributes:
        FIELDS               tuple of attributes a Currency object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = CurrencyController

    FIELDS = (
        BaseField("id", "id", aliases=["currencyId"], required=False),
        BaseField("factor", "factor", required=False),
        BaseField("symbol", "symbol", required=False),
        BaseField("isoCode", "isoCode", required=False),
        BaseField("shortName", "shortName", required=False),
        BaseField("name", "name", required=False),
        BaseField("decimalPrecision", "decimalPrecision", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
        BaseField("isSystemDefault", "isSystemDefault", required=False),
        BaseField("customFields", "customFields", required=False),
        BaseField("createdAt", "createdAt", required=False),
        BaseField("updatedAt", "updatedAt", required=False)
    )

    @staticmethod
    def convert(client, data, field, key):
        """
        converts the data to a queryset

        Parameters:
        client:             client object to connect with a shopware api
        data:               dictionary

        Returns:
        key, Queryset object

       """
        currency = data.get(key)

        if isinstance(currency, Currency):
            return "currency", currency
        elif key == "currencyId":
            model = client().controller.Currency.get(currency)
            return "currency", model
