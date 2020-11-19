#/api/v2/property-group/{uuid}/options
from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.property_option import PropertyOptionController
from shopwareapi.utils.queryset import Queryset
from shopwareapi.utils.converter import Convert

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
        BaseField("position", "position", required=False, converter=Convert.to_int),
    )

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
            model = PropertyOption(options={"client": client()})

            if isinstance(item, PropertyOption):
                result_models.append(item)

            else:
                model.map_attributes(item)
                result_models.append(model)

        return key, Queryset(PropertyOption, *result_models)
