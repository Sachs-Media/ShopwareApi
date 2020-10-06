from shopwareapi.core.basecontroller import BaseController


class ManufacturerController(BaseController):

    api_model = "product-manufacturer"

    def get_or_create(self, **kwargs):
        if len(self.find(self.model.name, matches_field="name").all()) > 0:
            return self.get(**kwargs)
        return self.create(**kwargs)
