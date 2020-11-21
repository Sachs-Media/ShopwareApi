

class QuerySet:

    def __init__(self, *args, **kwargs):
        self._model = kwargs.pop("model", None)

    def get(self, *args, **kwargs):

        print(args, kwargs)
