class LazyModel:

    def __init__(self, *args, model=None, **kwargs):
        self._model = model
        self._kwargs = kwargs
        self._converted = False
        name = model._meta.pk.name

        setattr(self, name, self._kwargs.get(name))

    def _get_pk_val(self, meta=None):
        return getattr(self, self._model._meta.pk.name)

    def __getattribute__(self, item):
        if item in ["load"] or item.startswith("_") or self._converted:
            return object.__getattribute__(self, item)
        else:
            raise AttributeError("Please use 'load' method first")

    def load(self, *args, **kwargs):
        if self._converted:
            return self

        val = None
        name = None

        for f in self._model._meta.fields:
            if f.primary_key is True:
                name = f.name
                val = self._kwargs.get(f.name)
        if val is None:
            raise ValueError("No PrimaryKey value found")
        return self._model.objects.get(**{name: val})