from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.custom_field import CustomFieldController


class CustomField(BaseModel):
    """
    model for a shopware CustomField

    Attributes:
        FIELDS               tuple of attributes a CustomField object has
        CONTROLLER_CLASS     specifies a controller class for this model
    """
    CONTROLLER_CLASS = CustomFieldController

    FIELDS = (
        BaseField("id", "id", required=False),
        BaseField("name", "name", required=False),
        BaseField("value", "value", required=False),
        BaseField("type", "type", required = False),
    )

