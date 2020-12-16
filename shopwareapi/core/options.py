from shopwareapi.client import ShopwareClient
from shopwareapi.core.field import BaseField
from shopwareapi.core.field import BaseRelationField

DEFAULT_NAMES = [
    "api_endpoint", "api_type", "swapi_client"
]


class Options:

    def __init__(self, meta):
        self.meta = meta
        self.pk = None
        self.lazy = False
        self.local_fields = []
        self.object_name = None
        self.swapi_client = None
        self.relation_fields = []
        self.manager = None
        self.api_endpoint = getattr(meta, "api_endpoint", None)
        self.api_type = getattr(meta, "api_type", None)
        self.original_attrs = {}

    @property
    def fields(self):
        return self.local_fields + self.relation_fields

    def contribute_to_class(self, cls, name):
        self.object_name = cls.__name__
        cls._meta = self
        self.model = cls
        self.original_attrs = {}

        # Next, apply any overridden values from 'class Meta'.
        if self.meta:

            meta_attrs = self.meta.__dict__.copy()

            for name in self.meta.__dict__:

                # Ignore any private attributes that Django doesn't care about.
                # NOTE: We can't modify a dictionary's contents while looping
                # over it, so we loop over the *original* dictionary instead.
                if name.startswith('_'):
                    del meta_attrs[name]

            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs))

        del self.meta

    def add_field(self, field, private=False):
        self.setup_pk(field)

        if isinstance(field, BaseRelationField):
            self.relation_fields.append(field)

        elif isinstance(field, BaseField):
            self.local_fields.append(field)
        else:
            raise ValueError("Field must be an instance from BaseField or BaseRelationField")

    def get_default(self):
        return None

    def set_manager(self, manager):
        self.manager = manager

    def setup_pk(self, field):
        if field.primary_key:
            self.pk = field

    def use(self, swapi_client: ShopwareClient):
        if isinstance(swapi_client, ShopwareClient):
            self.swapi_client = swapi_client
        else:
            ValueError("Client must be an instance of shopware.client.ShopwareClient class")
        return self.manager

    def lazy_load(self):

        data = self.model.objects.get(pk=getattr(self.model.concrete[self.pk.name]))

        for field in self.fields:
            try:
                delattr(self.model, field.name)
            except AttributeError:
                pass
            # getattr(self.model, field.name).fset(self, "asdfasdf")

            setattr(self.model, field.name, getattr(data, field.name))
            # setattr(self.model, field.name, getattr(data, field.name))

        self.lazy = False
        delattr(self.model, "__getattribute__")

    def set_lazy(self):
        self.lazy = True

        def def_getattr(*args, **kwargs):
            return super().__getattribute__(*args, **kwargs)

        def foo(self, name, **kwargs):
            result = object.__getattribute__(self, name)
            if name.startswith("_") or name in ["model", "concrete"]:
                return result

            if not isinstance(result, property):
                return result

            if object.__getattribute__(self, "_meta").lazy is True:
                setattr(self, "__getattribute__", def_getattr)
                object.__getattribute__(self, "_meta").lazy_load()
                return result
            else:
                return result

        setattr(self.model, "__getattribute__", foo)
        #
        #
        # def lazy_access(field):
        #     def wrapper(model):
        #         if self.lazy is True:
        #             return self.lazy_load(field)
        #         else:
        #             return getattr(self, field.name)
        #     return wrapper
        #
        # for field in self.fields:
        #     if not hasattr(self.model, field.name):
        #         setattr(self.model, field.name, property(lazy_access(field)))
        #     else:
        #         if getattr(self.model, field.name) is None:
        #             setattr(self.model, field.name, lazy_property(lazy_access(field)))
