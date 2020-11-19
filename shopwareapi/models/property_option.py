from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_option import PropertyOptionController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert
from shopwareapi.models.property_group import PropertyGroup


class PropertyOption(BaseModel):
    """
    model for a shopware PropertyOption
    /api/v2/property-group/{uuid}/options

    Attributes:
        FIELDS               tuple of attributes a PropertyOption object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyOptionController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
        BaseField("options", "options", related_to="self", nested=True, converter=PropertyGroup.convert),
    )
