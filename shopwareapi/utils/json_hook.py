from shopwareapi.utils.queryset import Queryset
import json


class ComplexEncoder(json.JSONEncoder):
    """
    Encoder for json.dumps()
    """
    def default(self, obj):
        if isinstance(obj, Queryset):
            result = []
            for item in obj:
                result.append(item.get_dict())
            return result

        return json.JSONEncoder.default(self, obj)
