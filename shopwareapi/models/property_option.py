#/api/v2/property-group/{uuid}/options
from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_option import PropertyOptionController


class PropertyOption(BaseModel):
    """
    model for a shopware PropertyOption

    Attributes:
        FIELDS               tuple of attributes a PropertyOption object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyOptionController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("position", "position", required=False),
    )
