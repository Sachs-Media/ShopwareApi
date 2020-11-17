from shopwareapi.core.basecontroller import BaseController, DictMode
from shopwareapi.utils.queryset import Queryset
from shopwareapi.models.custom_field import CustomField


class CustomFieldSetController(BaseController):
    api_model = "custom-field-set"

    def get_fields(self):
        request_url = self.get_client().build_url(model="custom-field-set/{}/custom-fields".format(self.model.id))
        result = self.get_client().get(request_url)
        result_list = []
        for item in result.get("data"):
            result_list.append(CustomField(id=item.get("id"), **item.get("attributes")))
        return Queryset(CustomField, *result_list)

    def add_field(self, field):
        if not field.name.startswith(self.model.name):
            raise ValueError("Name of Customfield must be prefixed with name of CustomFieldSet. Please change {} to {}_{}".format(field.name, self.model.name, field.name))
        request_url = self.get_client().build_url(model="custom-field-set/{}/custom-fields".format(self.model.id))
        self.get_client().post(request_url, field.get_dict(mode=DictMode.WRITE))
