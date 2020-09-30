import shopwareapi.exception as exception
import shopwareapi.utils.map as maputil


class BaseModel(maputil.AttributeMixin):
    
    CONTROLLER_CLASS = None
    
    FIELDS = None

    def __init__(self, **kwargs):

        if not self.__class__.CONTROLLER_CLASS:
            raise RuntimeError("Every model must defined a CONTROLLER; this is no fault of yours, but the fault of the libary developer ")
        self.controller = self.__class__.CONTROLLER_CLASS(self)

        self._options = kwargs.pop("options", self.get_options())

        self._client = self._options.get("client")
        self.map_attributes(kwargs)
        
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
        
    def get_fields(self):
        if self.__class__.FIELDS is None:
            raise ValueError("Fields must be contains BaseField definitions")
        else:
            return self.__class__.FIELDS

    def get_dict(self, data=None):
        """
            Returns current Model object as dict
            :return dict: dict representation of current object
        """

        if data is None:
            data = dict()
        for field in self.get_fields():
            if hasattr(self, field.attribute_name):
                value = getattr(self, field.attribute_name)
                if field.nested:
                    # find fields which are related to the nested field
                    related_fields = list(
                        filter(lambda item: item.related_to == field.attribute_name, self.get_fields())
                    )
                    data.update(value.parent_update(data, related_fields))
                else:
                    if value is not None:
                        data[field.api_name] = value
            elif field.required and not hasattr(self, field.attribute_name):
                raise ValueError("The parameter {} is required".format(field.attribute_name))

        return data

    def parent_update(self, data, related_fields):
        new_data = {}
        for field in related_fields:
            local_field_list = list(
                set(
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
            )

            if len(local_field_list) > 1:
                raise ValueError("Multiple fields have the same alias, apiname or name")

            local_field = local_field_list[0]
            if hasattr(self, local_field.attribute_name):
                new_data[field.api_name] = getattr(self, local_field.attribute_name)
        return new_data
