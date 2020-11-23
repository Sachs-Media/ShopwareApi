

class QuerySet:

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)

    def get(self, *args, **kwargs):
        # print(self.model._meta.api_endpoint)
        print(self.model._meta.__dict__)