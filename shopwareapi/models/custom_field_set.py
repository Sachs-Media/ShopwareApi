from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.custom_field_set import CustomFieldSetController
from shopwareapi.models.custom_field_set_relation import CustomFieldSetRelation
from shopwareapi.models.custom_field import CustomField


class CustomFieldSet(BaseModel):
    """
        model for a shopware CustomField Set
    """
    CONTROLLER_CLASS = CustomFieldSetController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("relations", "relations", nested=True, related_to="self", converter=CustomFieldSetRelation.convert_queryset, secondary_converter=CustomFieldSetRelation.convert_only_from_queryset("entityName"), required=False),
        BaseField("fields", "fields", nested=True, related_to=CustomField, required=False),
    )