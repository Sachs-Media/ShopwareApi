
DEFAULT_NAMES = [
    "api_endpoint", "api_type", "swapi_client"
]


class Options:

    def __init__(self, meta):
        self.meta = meta
        self.pk = None
        self.local_fields = []
        self.swapi_client = None
        self.relation_fields = []
        self.local_manager = None
        self.api_endpoint = None
        self.api_type = None
        self.original_attrs = {}

    @property
    def fields(self):
        return self.local_fields + self.relation_fields

    def contribute_to_class(self, cls, name):
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
        self.local_fields.append(field)

    def get_default(self):
        return None

    def _prepare(self, model):

        if self.pk is None:
            for field in self.fields:
                self.setup_pk(field)

    def set_manager(self, manager):
        self.local_manager = manager

    def setup_pk(self, field):
        if not self.pk and field.primary_key:
            self.pk = field
