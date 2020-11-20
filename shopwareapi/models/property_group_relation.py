from shopwareapi.controller.property_group_relation import PropertyGroupRelationController
from shopwareapi.core.basefield import BaseField
from shopwareapi.utils.queryset import Queryset
from shopwareapi.core.basemodel import BaseModel


class PropertyGroupRelation(BaseModel):
    """
    model for a shopware PropertyGroupRelation

    Attributes:
        FIELDS               tuple of attributes a PropertyGroupRelation object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = PropertyGroupRelationController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("entityName", "entityName", required=False),
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

            model = PropertyGroupRelation(options={"client": client()})
            if isinstance(item, PropertyGroupRelation):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)
        return key, Queryset(PropertyGroupRelation, *result_models)
