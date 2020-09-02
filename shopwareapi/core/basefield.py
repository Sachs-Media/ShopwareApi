from shopwareapi.utils.converter import Convert


class BaseField:

    def __init__(self, attribute_name=None, api_name=None, aliases=None, converter=None, required=False, nested=False, related_to=None):
        if aliases is None:
            aliases = []
        if converter is None:
            converter = Convert.to_string
        
        self.attribute_name = attribute_name
        self.api_name = api_name 
        self.aliases = aliases
        self.converter = converter 
        self.required = required
        self.related_to = related_to
        self.nested = nested