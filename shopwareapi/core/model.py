from shopwareapi.core.query import QuerySet
import inspect
from shopwareapi.core.options import Options
from shopwareapi.core.manager import Manager


def _has_contribute_to_class(value):
    # Only call contribute_to_class() if it's bound.
    return not inspect.isclass(value) and hasattr(value, 'contribute_to_class')


class MetaModel(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__

        # Extract module and meta
        module = attrs.pop('__module__')
        attr_meta = attrs.pop('Meta', None)
        # Create new objects attrs
        new_attrs = {'__module__': module}

        contributable_attrs = {}

        for attr_name, attr_value in attrs.items():
            if _has_contribute_to_class(attr_value):
                # memory Own things
                contributable_attrs[attr_name] = attr_value
            else:
                # Assign Strange field to Model instance
                new_attrs[attr_name] = attr_value

        # create new object
        new_class = super_new(cls, name, bases, attrs, **kwargs)

        # get meta class from object
        meta = attr_meta or getattr(new_class, 'Meta', None)
        # assign Options to Object
        new_class.add_to_class('_meta', Options(meta))

        # Assign fields to Object
        for attr_name, attr_value in contributable_attrs.items():
            new_class.add_to_class(attr_name, attr_value)

        # Initialize Object
        new_class._prepare()
        return new_class

    def _prepare(cls):
        """Create some methods once self._meta has been populated."""
        # Initialize Options
        opts = cls._meta
        opts._prepare(cls)

        # Check if any field has same name like Manager
        if any(f.name == 'objects' for f in opts.fields):
            raise ValueError(
                "Model %s must specify a custom Manager, because it has a "
                "field named 'objects'." % cls.__name__
            )
        # Initialize Manager
        manager = Manager()
        # Assign Manager to Object
        cls.add_to_class('objects', manager)

    def add_to_class(cls, name, value):
        if _has_contribute_to_class(value):
            # Assign api objects via contribute_to_class
            value.contribute_to_class(cls, name)
        else:
            # Assign strange attributes directly
            setattr(cls, name, value)


class Model(metaclass=MetaModel):

    def __init__(self, *args, **kwargs):
        opts = self._meta
        _setattr = setattr

        fields_iter = iter(opts.fields)

        for field in fields_iter:
            val = field.get_default()
            if kwargs:
                if field.name in kwargs:
                    val = kwargs.pop(field.name)

            _setattr(self, field.name, val)
        super().__init__()

    def _get_pk_val(self, meta=None):
        meta = meta or self._meta
        return getattr(self, meta.pk.attname)

    def _set_pk_val(self, value):
        for parent_link in self._meta.parents.values():
            if parent_link and parent_link != self._meta.pk:
                setattr(self, parent_link.target_field.attname, value)
        return setattr(self, self._meta.pk.attname, value)

    pk = property(_get_pk_val, _set_pk_val)
