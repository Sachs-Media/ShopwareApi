import json


class QuerySet:

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        self.filter_query = kwargs.pop("filter_query", dict())
        self._result_cache = kwargs.pop("results", None)

    def __len__(self):
        return len(self._result_cache)

    def __iter__(self):
        return iter(self._result_cache)

    def get(self, *args, **kwargs):
        # print(self.model._meta.api_endpoint)

        filter_result = self.filter(**kwargs)
        num = len(filter_result)
        if num == 1:
            return filter_result.first()
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

        return self._chain(_result_cache=results)

    def first(self, *args, **kwargs):
        return self._result_cache[0]

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj._meta.use(self.model._meta.swapi_client)
        obj.create(force=True)
        return obj

    def update(self, **kwargs):
        obj = self.model(**kwargs)
        obj._meta.use(self.model._meta.swapi_client)
        obj.update(force=True)
        return obj

    def update_filter_query(self, **kwargs):
        query = self.filter_query.copy()

        if self._result_cache:
            query.update({
                "id": [item.id for item in self._result_cache]
            })

        includes = {}
        for related_field in self.model._meta.relation_fields:
            model = related_field.get_related_model_class()
            includes[related_field.name] = ["id"]

        if includes:
            query.update({"includes": includes})

        filter = []

        for field in self.model._meta.fields:

            if field.name in kwargs:
                search_value = kwargs.get(field.name)

                filter.append({
                    "type": "equals",
                    "field": field.attname,
                    "value": field.to_simple(search_value)
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
