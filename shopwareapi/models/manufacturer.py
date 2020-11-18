from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.manufacturer import ManufacturerController


class Manufacturer(BaseModel):
    """
    model for a shopware Manufacturer

    Attributes:
        FIELDS               tuple of attributes a Manufacturer object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = ManufacturerController

    FIELDS = (
        BaseField("id", "id", aliases=["manufacturerId"], required=False),
        BaseField("name", "name", required=False),
        BaseField("mediaId", "mediaId", required=False),
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
        manufacturer = data.get(key)

        if isinstance(manufacturer, Manufacturer):
            return "manufacturer", manufacturer
        elif key == "manufacturerId":
            model = client().controller.Manufacturer.get(manufacturer)
            return "manufacturer", model
