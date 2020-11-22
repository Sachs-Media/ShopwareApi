

class QuerySet:

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self._model = kwargs.pop("model", None)
        self.swapi_client = kwargs.pop("swapi_client", None)

    def get(self, *args, **kwargs):
        print(self._model._meta.api_endpoint)
        print(self.swapi_client.post())
