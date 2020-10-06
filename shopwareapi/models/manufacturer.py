from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.manufacturer import ManufacturerController
from shopwareapi.utils.converter import Convert


class Manufacturer(BaseModel):
    CONTROLLER_CLASS = ManufacturerController

    FIELDS = (
        BaseField("id", "id", aliases=["manufacturerId"], required=False),
        BaseField("name", "name", required=False),
    )

    @staticmethod
    def convert(client, data, field, key):
        manufacturer = data.get(key)

        if isinstance(manufacturer, Manufacturer):
            return "manufacturer", manufacturer
        elif key == "manufacturerId":
            model = client().controller.Manufacturer.get(manufacturer)
            return "manufacturer", model
