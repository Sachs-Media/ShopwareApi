import shopwareapi.exception as exception
import shopwareapi.utils.map as maputil
from shopwareapi.utils.helper import deduplicate
import enum


class DictMode(enum.Enum):
    ALL = "all"
    WRITE = "write"


class BaseModel(maputil.AttributeMixin):
    
    CONTROLLER_CLASS = None
    
    FIELDS = None

    def __init__(self, **kwargs):

        if not self.__class__.CONTROLLER_CLASS:
            raise RuntimeError("every model must define a CONTROLLER_CLASS")
        self.controller = self.__class__.CONTROLLER_CLASS(self)

        self._options = kwargs.pop("options", self.get_options())

        self._client = self._options.get("client")
        self.map_attributes(kwargs)

    @classmethod
    def find_field(cls, needle):
        """
            Helper method to find a "needle" in STRUCTURE.
            This method try to match needle with field (key), one of field aliases field.apiname or field.name
            :param needle: word/attribute which should be found in structure
            :return:
        """
        for field in cls.get_fields():
            if needle in field.aliases or \
                    needle == field.attribute_name or \
                    needle == field.api_name:
                return field

    def get_client(self):
        if not self._client:
            raise exception.NotConnectedToClient("Please link this to ShopwareClient object. Using client.send(<thisobject>) ")
        return self._client

    def use_client(self, client):

        if self._client is None:
            self._client = client
        else:
            raise exception.AlreadyConnected("Another ShopwareClient is linked to this Model")

    @staticmethod
    def convert(client, data, field, key):
        """
        This method should be used by ShopwareTranslate to Convert a attribute to a submodal
        
        :return:
        """
        raise NotImplemented("This method is currently not implemented")

    def get_options(self):
        return {}

    @classmethod
    def get_fields(cls):
        if cls.FIELDS is None:
            raise ValueError("Fields must be contains BaseField definitions")
        else:
            return cls.FIELDS

    def get_dict(self, data=None, mode=DictMode.ALL):
        """
            Returns current Model object as dict
            :return dict: dict representation of current object
        """
        if data is None:
            data = dict()
        for field in self.get_fields():
            if mode == DictMode.ALL:

                if hasattr(self, field.attribute_name):
                    value = getattr(self, field.attribute_name)
                    if field.nested:
                        # find fields which are related to the nested field
                        related_fields = list(
                            filter(lambda item: item.related_to == field.attribute_name, self.get_fields())
                        )
                        if field.related_to == "self":
                            related_fields.append(field)

                        data.update(value.parent_update(data, related_fields, self))
                    else:
                        if value is not None:
                            data[field.api_name] = value
                elif field.required and not hasattr(self, field.attribute_name):
                    raise ValueError("The parameter {} is required".format(field.attribute_name))

            elif mode == DictMode.WRITE:
                if not field.read_only:

                    if hasattr(self, field.attribute_name):
                        value = getattr(self, field.attribute_name)
                        if field.nested:
                            # find fields which are related to the nested field
                            related_fields = list(
                                filter(lambda item: item.related_to == field.attribute_name, self.get_fields())
                            )
                            if field.related_to == "self":
                                related_fields.append(field)
                            data.update(value.parent_update(data, related_fields, self))
                        else:
                            if value is not None:
                                data[field.api_name] = value
                    elif field.required and not hasattr(self, field.attribute_name):
                        raise ValueError("The parameter {} is required".format(field.attribute_name))

        return data

    def parent_update(self, data, related_fields, remote_obj):
        new_data = {}
        for field in related_fields:
            local_field_list = set(
                filter(
                    lambda item: item is not None,
                    [
                        self.find_field(field.api_name),
                        self.find_field(field.attribute_name)
                    ] +
                    [
                        self.find_field(alias) for alias in field.aliases
                    ]
                )
            )

            if field.related_to == "self":
                local_field_list.add(field)

            local_field_list = deduplicate(list(local_field_list))

            if len(local_field_list) > 1:
                raise ValueError("Multiple fields have the same alias, apiname or name")

            local_field = local_field_list[0]
            if hasattr(self, local_field.attribute_name):
                new_data[field.api_name] = getattr(self, local_field.attribute_name)
                if field.secondary_converter is not None:
                    new_data[field.api_name] = field.secondary_converter(self, field, local_field)
        return new_data

    @classmethod
    def convert_only_from_queryset(cls, *field_name_list):

        def wrapper(queryset, field, local_field, *args, **kwargs):
            result = []
            for item in queryset:
                for name in field_name_list:
                    result.append({name: getattr(item, name)})
            return result

        return wrapper