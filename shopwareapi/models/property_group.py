from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_group import PropertyGroupController
from shopwareapi.models.property_group_relation import PropertyGroupRelation
from shopwareapi.utils.converter import Convert


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
        BaseField("filterable", "filterable", required=False, converter=Convert.to_boolean),
        BaseField("sortingType", "sortingType", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
        BaseField("relations", "relations", nested=True, related_to="self", converter=PropertyGroupRelation.convert_queryset, secondary_converter=PropertyGroupRelation.convert_only_from_queryset("entityName"), required=False),
    )
