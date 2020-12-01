import inspect


class NOT_PROVIDED:
    pass


def return_None():
    return None


class BaseField:

    def __init__(self, name=None, aliases=NOT_PROVIDED, primary_key=False,
                 max_length=None, blank=False, null=False,
                 rel=None, default=NOT_PROVIDED, editable=True, choices=None, help_text='', validators=()):
        self.name = name
        self.aliases = aliases
        self.primary_key = primary_key
        self.max_length = max_length
        self.blank = blank
        self.null = null
        self.rel = rel
        self.default = default
        self.editable = editable
        self.choices = choices
        self.help_text = help_text
        self.validators = validators
        super().__init__()

    def has_default(self):
        """Return a boolean of whether this field has a default value."""
        return self.default is not NOT_PROVIDED

    def get_default(self):
        """Return the default value for this field."""
        return self._get_default()()

    def _get_default(self):

        if self.has_default():
            if callable(self.default):
                return self.default
            return lambda: self.default

        if self.null:
            return return_None

        return str  # return empty string

    def to_python(self, value):
        pass

    def get_attname(self):
        return self.name

    def set_attributes_from_name(self, name):
        self.name = self.name or name
        self.attname = self.get_attname()

    def contribute_to_class(self, cls, name, private_only=False):
        """
            Register the field with the model class it belongs to.
            If private_only is True, create a separate instance of this field
            for every subclass of cls, even if cls is not an abstract model.
        """
        self.model = cls
        self.set_attributes_from_name(name)
        cls._meta.add_field(self, private=private_only)


class BaseRelationField(BaseField):

    def __init__(self, to, **kwargs):
        self.related_name = kwargs.pop("related_name", "")
        super().__init__(**kwargs)
        self.to = to
        #print(inspect.getmro(self.__class__))
        #class_lookups = [parent for parent in inspect.getmro(self.model.__class__)]
        #print(class_lookups)

        #
        # rel = self.rel_class(
        #     self, to,
        #     related_name=related_name
        # )

    def get_related_model_class(self):
        if isinstance(self.to, str) and not hasattr(self, "related_model"):
            name = "shopwareapi.api.{}".format(self.to)
            components = name.split(".")
            mod = __import__(".".join(components[:-1]), fromlist=components[-1:])
            model = getattr(mod, components[-1:][0])
            # model.objects.use(self.model._meta.swapi_client)
            self.related_model = model
            return model

        elif hasattr(self, "related_model"):
            return self.related_model
        else:
            return self.to