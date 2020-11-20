from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_group import PropertyGroupController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert
from shopwareapi.models.property_option import PropertyOption


class PropertyGroup(BaseModel):
    """
    model for a shopware PropertyGroup

    Attributes:
        FIELDS               tuple of attributes a PropertyGroup object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyGroupController

    FIELDS = (
        BaseField("id", "id", aliases=["propertygroupId"], required=False),
        BaseField("name", "name", required=False),
        BaseField("description", "description", required=False),
        BaseField("displayType", "displayType", required=False),
        BaseField("filterable", "filterable", required=False, converter=Convert.to_boolean),
        BaseField("sortingType", "sortingType", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
    )

    @staticmethod
    def convert(client, data, field, key):
        propertygroup = data.get(key)

        if isinstance(propertygroup, PropertyGroup):
            return "propertygroup", propertygroup
        elif key == "propertygroupId":
            model = client().controller.PropertyGroup.get(propertygroup)
            return "propertygroup", model

    @staticmethod
    def convert_queryset(client, data, field, key):
        """
        converts the data to a queryset

        Parameters:
        client:             client object to connect with a shopware api
        data:               dictionary

        Returns:
        key, Queryset object

       """
        result_models = []

        for item in data.get(key):
            model = PropertyGroup(options={"client": client()})

            if isinstance(item, PropertyGroup):
                result_models.append(item)

            else:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(PropertyGroup, *result_models)
