from shopwareapi.controller.custom_field_set_releation import CustomFieldSetRelationController
from shopwareapi.core.basefield import BaseField
from shopwareapi.utils.queryset import Queryset
from shopwareapi.core.basemodel import BaseModel


class CustomFieldSetRelation(BaseModel):
    CONTROLLER_CLASS = CustomFieldSetRelationController

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

            model = CustomFieldSetRelation(options={"client": client()})
            if isinstance(item, CustomFieldSetRelation):
                result_models.append(item)
            else:
                model.map_attributes(item)
                result_models.append(model)
        return key, Queryset(CustomFieldSetRelation, *result_models)



