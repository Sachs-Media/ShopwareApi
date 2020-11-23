

class QuerySet:

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        self.swapi_client = kwargs.pop("swapi_client", None)

    def get(self, *args, **kwargs):
        #print(self.model.__dict__)
        #print(self.model._meta.local_manager.swapi_client)
        # print(self.swapi_client.post(url={
        #     "model": self.model._meta.api_endpoint
        # }))
        print(self.model._meta.meta.__dict__)
        #self.swapi_client.post(url)