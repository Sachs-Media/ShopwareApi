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

    def has_default(self):
        """Return a boolean of whether this field has a default value."""
        return self.default is not NOT_PROVIDED

    def get_default(self):
        """Return the default value for this field."""
        return self._get_default()

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

    def contribute_to_class(self, cls, name, private_only=False):
        """
            Register the field with the model class it belongs to.
            If private_only is True, create a separate instance of this field
            for every subclass of cls, even if cls is not an abstract model.
        """
        self.name = self.name or name
        self.model = cls
        cls._meta.add_field(self, private=private_only)
