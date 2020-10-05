from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.manufacturer import ProductManufacturerController
from shopwareapi.utils.converter import Convert


class ProductManufacturer(BaseModel):
    CONTROLLER_CLASS = ProductManufacturerController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
    )

    @staticmethod
    def convert(client, data, field, key):
        manufacturer = data.get(key)

        if isinstance(manufacturer, ProductManufacturer):
            return "manufacturer", manufacturer
        elif key == "manufacturerId":
            model = client().controller.ProductManufacturerController.get(manufacturer)
            return "manufacturer", model
