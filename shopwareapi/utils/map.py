import logging

log = logging.getLogger(__name__)


class AttributeMixin(object):
    """
        Mixin for helper methods for working with Object attributes
    """

    def map_attributes(self, data):

        if type(data) == list:
            items = data
        else:
            items = data.items()

        for key, item in items:

            field = self.__class__.find_field(key)

            if field is not None:
                if data[key] is None:
                    setattr(self, key, None)
                else:
                    converted_information = field.converter(self.get_client, data, field, key)
                    if converted_information is not None:
                        setattr(self, *converted_information)
