from shopwareapi.exceptions import ParameterError

class QuerySet:

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        self._result_cache = None

    def get(self, *args, **kwargs):
        # print(self.model._meta.api_endpoint)

        if ("id" in kwargs or "pk" in kwargs) and len(kwargs) > 1:
            raise ParameterError("If id or pk are given only one of this two are allowed")

        pk = kwargs.get("pk") or getattr(self.model, "pk")

        self.model._meta.swapi_client.get(url={
            "model": (self.model._meta.api_endpoint, pk)
        })

        if num == 1:
            return clone._result_cache[0]
        if not num:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        raise self.model.MultipleObjectsReturned(
            'get() returned more than one %s -- it returned %s!' % (
                self.model._meta.object_name,
                num if not limit or num < limit else 'more than %s' % (limit - 1),
            )
        )


    def filter(self, *args, **kwargs):

        if self._result_cache is None:
            # Online Filter





        else:
            # filter in _cache


    def find(self, **kwargs):
        """
            Find Attributes by specified kwargs

            :param kwargs:
            :return:
        """
