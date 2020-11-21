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

        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        attr_meta = attrs.pop('Meta', None)

        contributable_attrs = {}

        for attr_name, attr_value in attrs.items():
            if _has_contribute_to_class(attr_value):
                # Own things
                contributable_attrs[attr_name] = attr_value
            else:
                # Strange field
                new_attrs[attr_name] = attr_value

        new_class = super_new(cls, name, bases, attrs, **kwargs)

        meta = attr_meta or getattr(new_class, 'Meta', None)
        new_class.add_to_class('_meta', Options(meta))

        for attr_name, attr_value in contributable_attrs.items():
            new_class.add_to_class(attr_name, attr_value)

        new_class._prepare()
        return new_class

    def _prepare(cls):
        """Create some methods once self._meta has been populated."""
        opts = cls._meta
        opts._prepare(cls)

        if any(f.name == 'objects' for f in opts.fields):
            raise ValueError(
                "Model %s must specify a custom Manager, because it has a "
                "field named 'objects'." % cls.__name__
            )
        manager = Manager()
        manager.auto_created = True
        cls.add_to_class('objects', manager)



    def add_to_class(cls, name, value):
        if _has_contribute_to_class(value):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Model(metaclass=MetaModel):

    def __init__(self, **kwargs):
        opts = self._meta
        _setattr = setattr

        fields_iter = iter(opts.fields)

        for field in zip(fields_iter):
            val = field.get_default()

            if kwargs:
                if field.name in kwargs:
                    val = kwargs.pop(field.name)

            _setattr(self, field.name, val)

    @classmethod
    def _check_managers(cls, **kwargs):
        """Perform all manager checks."""
        errors = []
        for manager in cls._meta.managers:
            errors.extend(manager.check(**kwargs))
        return errors
