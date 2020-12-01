import json


class QuerySet:

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        self.filter_query = kwargs.pop("filter_query", dict())
        self._result_cache = kwargs.pop("results", None)

    def get(self, *args, **kwargs):
        # print(self.model._meta.api_endpoint)

        filter_result = self.filter(**kwargs)

        num = len(filter_result)
        if num == 1:
            return filter_result[0]
        if not num:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        raise self.model.MultipleObjectsReturned(
            'get() returned more than one %s -- it returned %s!' % (
                self.model._meta.object_name,
                num,
            )
        )

    @classmethod
    def _normalize_response(cls, item):
        result = {"id": item.get("id")}
        result.update(item.get("attributes"))
        return result

    def filter(self, **kwargs):
        """
            Find Attributes by specified kwargs

            :param kwargs:
            :return:
        """
        self.update_filter_query(**kwargs)

        result_response = self.model._meta.swapi_client.post(url={
            "model": ("search", self.model._meta.api_endpoint),
        }, data=json.dumps(self.filter_query))

        results = []
        for item in result_response.get("data"):
            results.append(self.model.from_api(self._normalize_response(item), self.model._meta))
        return self._chain(results=results)

    def update_filter_query(self, **kwargs):
        query = self.filter_query.copy()

        if self._result_cache:
            query.update({
                "id": [item.id for item in self._result_cache]
            })

        includes = {}
        for related_field in self.model._meta.relation_fields:
            model = related_field.get_related_model_class()
            print(model, related_field.name, self.model)
            includes[model._meta.api_type] = ["id"]

        if includes:
            query.update({"includes": includes})

        filter = []
        for field_name, search_value in kwargs.items():

            if field_name == "pk":
                field_name = self.model._meta.pk.name

            filter.append({
                "type": "equals",
                "field": field_name,
                "value": search_value
            })
        if filter:
            query.update({"filter": filter})

        self.filter_query.update(query)

    def _clone(self):
        """
            Return a copy of the current QuerySet. A lightweight alternative
            to deepcopy().
        """
        c = self.__class__(model=self.model, filter_query=self.filter_query)
        return c

    def _chain(self, **kwargs):
        """
        Return a copy of the current QuerySet that's ready for another
        operation.
        """
        obj = self._clone()
        obj.__dict__.update(kwargs)
        return obj
