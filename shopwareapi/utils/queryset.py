from shopwareapi.utils.helper import deduplicate
from shopwareapi.exception import NotEnoughItems


class Queryset:

    def __str__(self):
        return "<Queryset {} >".format(self._model_list)


    def __init__(self, model, *args):
        self._model = model

        for item in args:

            if not isinstance(item, self._model):
                raise ValueError("A Queryset can only contain objects from same model.", item)

        self._model_list = args

    def __iter__(self):
        for x in self._model_list:
            yield x

    def __len__(self):
        return len(self._model_list)

    def all(self):
        return self._model_list

    def parent_update(self, data, related_fields, remote_obj):
        new_data = {}
        for field in related_fields:
            local_field_list = set(
                    filter(
                        lambda item: item is not None,
                        [
                            self._model.find_field(field.api_name),
                            self._model.find_field(field.attribute_name)
                        ] +
                        [
                            self._model.find_field(alias) for alias in field.aliases
                        ]
                    )
                )

            if field.related_to == "self":
                local_field_list.add(field)

            local_field_list = deduplicate(list(local_field_list))
            if len(local_field_list) > 1:
                raise ValueError("Multiple fields have the same alias, apiname or name")

            local_field = local_field_list[0]
            if hasattr(remote_obj, local_field.attribute_name):
                new_data[field.api_name] = getattr(remote_obj, local_field.attribute_name)
                if field.secondary_converter is not None:
                    new_data[field.api_name] = field.secondary_converter(self, field, local_field)
        return new_data

    def first(self):
        if len(self._model_list) > 0:
            return self._model_list[0]
        else:
            raise NotEnoughItems("couldn't find the first element")
