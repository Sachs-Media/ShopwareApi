import logging

log = logging.getLogger("shopwareapi.utils")


class AttributeMixin(object):
    """
        Mixin for helper methods for working with Object attributes
    """

    def find_field(self, needle):
        """
            Helper method to find a "needle" in STRUCTURE.
            This method try to match needle with field (key), one of field aliases field.apiname or field.name
            :param needle: word/attribute which should be found in structure
            :return:
        """
        for field in self.get_fields():
            if needle in field.aliases or \
               needle == field.attribute_name or \
               needle == field.api_name:
                return field

    def map_attributes(self, data):
        if type(data) == list:
            items = data
        else:
            items = data.items()
        for key, item in items:
            field = self.find_field(key)
            if field is None:
                log.debug("Attribute Mapping: Ignore parameter '{}'".format(key))
            else:
                if data[key] is None:
                    setattr(self, key, None)
                else:
                    converted_information = field.converter(self.get_client, data, field, key)
                    setattr(self, *converted_information)
