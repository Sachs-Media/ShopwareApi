from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_option import PropertyOptionController
from shopwareapi.utils.converter import Convert


class PropertyOption(BaseModel):
    """
    model for a shopware PropertyOption
    /api/v3/property-group/{uuid}/options
    /api/v3/search/property-group/{uuid}/options

    Attributes:
        FIELDS               tuple of attributes a PropertyOption object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyOptionController

    FIELDS = (
        BaseField("id", "id", aliases=["propertyoptionId"], required=False),
        BaseField("name", "name", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
    )

    @staticmethod
    def convert(client, data, field, key):
        propertyoption = data.get(key)

        if isinstance(propertyoption, PropertyOption):
            return "propertyoption", propertyoption
        elif key == "propertyoptionId":
            model = client().controller.PropertyOption.get(propertyoption)
            return "propertyoption", model