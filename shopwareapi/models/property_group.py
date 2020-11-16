#/api/v2/search/property-group
from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_group import PropertyGroupController


class PropertyGroup(BaseModel):
    """
    model for a shopware PropertyGroup

    Attributes:
        FIELDS               tuple of attributes a PropertyGroup object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyGroupController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("description", "description", required=False),
        BaseField("displayType", "displayType", required=False),
        BaseField("filterable", "filterable", required=False),
        BaseField("sortingType", "sortingType", required=False),
        BaseField("position", "position", required=False),
    )
