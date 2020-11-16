from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.tax import TaxController


class Tax(BaseModel):
    """
    model for a shopware Tax

    Attributes:
        FIELDS               tuple of attributes a Tax object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = TaxController

    FIELDS = (
        BaseField("id", "id", aliases=["taxId"], required=False),
        BaseField("taxRate", "taxRate", required=False),
        BaseField("name", "name", required=False)
    )

    @staticmethod
    def convert(client, data, field, key):
        """
        converts the model to id

        Parameters:
        client:             client object to connect with a shopware api
        data:               dictionary

        Returns:
        tax, model

       """
        tax = data.get(key)

        if isinstance(tax, Tax):
            return "tax", tax
        elif key == "taxId":
            model = client().controller.Tax.get(tax)
            return "tax", model
