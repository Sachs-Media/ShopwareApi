import sys
import copy


class NOT_PROVIDED:
    pass


def return_None():
    return None


class BaseField:

    def __init__(self, name=None, aliases=NOT_PROVIDED, primary_key=False,
                 max_length=None, null=False,
                 rel=None, default=NOT_PROVIDED, editable=True, choices=None, help_text='', validators=(),
                 read_only=False, attname=None):
        self.name = name
        self.attname = attname
        self.read_only = read_only
        self.aliases = aliases
        self.primary_key = primary_key
        self.max_length = max_length
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
        return value

    def clean(self, value):
        return self.to_python(value)

    def get_attname(self):
        return self.name or self.attname

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

    def to_simple(self, value):
        return value


class BaseRelationField(BaseField):

    def __init__(self, to, **kwargs):
        self.related_name = kwargs.pop("related_name", "")
        self.to = to
        super().__init__(**kwargs)
        if not self.null:
            self.related_model = self.get_related_model_class()

    def contribute_to_class(self, cls, name, private_only=False):
        super(BaseRelationField, self).contribute_to_class(cls, name, private_only=False)

    @property
    def remote_field(self):
        return self.related_model._meta.pk

    def get_attname(self):
        return "%sId" % self.name

    def get_related_model_class(self):

        if isinstance(self.to, str) and not hasattr(self, "related_model"):
            if self.to == "self":
                self.model._reverse.append(self)
                self.related_model = self.model
                return self.model
            else:
                name = "shopwareapi.api.{}".format(self.to)
                components = name.split(".")
                mod = __import__(".".join(components[:-1]), fromlist=components[-1:])
                model = getattr(mod, components[-1:][0])
                self.related_model = model
                model._reverse.append(self)
                return model

        elif hasattr(self, "related_model"):
            return self.related_model
        else:
            return self.to
