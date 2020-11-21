

class Options:

    def __init__(self, meta):
        self.meta = meta
        self.pk = None
        self.local_fields = []
        self.local_manager = None

    @property
    def fields(self):
        return self.local_fields

    def contribute_to_class(self, cls, name):
        cls._meta = self

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
