from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.custom_field import CustomFieldController


class CustomField(BaseModel):
    CONTROLLER_CLASS = CustomFieldController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("value", "value", required=False),
        BaseField("type", "type", required = False),
    )

