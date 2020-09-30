from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.tax import TaxController


class Tax(BaseModel):
    CONTROLLER_CLASS = TaxController

    FIELDS = (
        BaseField("id", "id", aliases=["taxId"], required=False),
        BaseField("taxRate", "taxRate", required=False),
        BaseField("name", "name", required=False)
    )

    @staticmethod
    def convert(client, data, field, key):
        tax = data.get(key)

        if isinstance(tax, Tax):
            return "tax", tax
        elif key == "taxId":
            model = client().controller.Tax.get(tax)
            return "tax", model
