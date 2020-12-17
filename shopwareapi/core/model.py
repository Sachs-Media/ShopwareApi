import json

from shopwareapi.core.field import BaseRelationField
from shopwareapi.core.manager import Manager
from shopwareapi.core.options import Options
from shopwareapi.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from shopwareapi.utils.helper import has_contribute_to_class, subclass_exception
import logging
import inspect

log = logging.getLogger(__name__)


class ModelBase(type):

    def __new__(cls, name, bases, attrs, **kwargs):

        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        # Extract module and meta
        module = attrs.pop('__module__')
        attr_meta = attrs.pop('Meta', None)

        # Create new objects attrs
        new_attrs = {'__module__': module, "concrete": dict(), "_reverse": []}

        contributable_attrs = {}

        for attr_name, attr_value in attrs.items():

            if has_contribute_to_class(attr_value):
                # memory Own things
                contributable_attrs[attr_name] = attr_value
            else:
                # Assign Strange field to Model instance
                new_attrs[attr_name] = attr_value

        # create new object
        new_class = super_new(cls, name, bases, new_attrs, **kwargs)

        # get meta class from object
        meta = attr_meta or getattr(new_class, 'Meta', None)

        # assign Options to Object
        new_class.add_to_class('_meta', Options(meta))

        # Assign fields to Object
        for attr_name, attr_value in contributable_attrs.items():
            new_class.add_to_class(attr_name, attr_value)

        new_class.add_to_class(
            'DoesNotExist',
            subclass_exception(
                'DoesNotExist',
                tuple(
                    x.DoesNotExist for x in parents if hasattr(x, '_meta')
                ) or (ObjectDoesNotExist,),
                module,
                attached_to=new_class))
        new_class.add_to_class(
            'MultipleObjectsReturned',
            subclass_exception(
                'MultipleObjectsReturned',
                tuple(
                    x.MultipleObjectsReturned for x in parents if hasattr(x, '_meta')
                ) or (MultipleObjectsReturned,),
                module,
                attached_to=new_class))

        # Initialize Object
        new_class._prepare()
        return new_class

    def _prepare(cls):
        """Create some methods once self._meta has been populated."""
        # Initialize Options
        opts = cls._meta

        # Check if any field has same name like Manager
        if any(f.name == 'objects' for f in opts.fields):
            raise ValueError(
                "Model %s must specify a custom Manager, because it has a "
                "field named 'objects'." % cls.__name__
            )
        # Assign Manager to Object
        cls.add_to_class('objects', Manager())

    def add_to_class(cls, name, value):
        if has_contribute_to_class(value):
            # Assign api objects via contribute_to_class
            value.contribute_to_class(cls, name)
        else:
            # Assign strange attributes directly
            setattr(cls, name, value)


class Model(metaclass=ModelBase):

    def __init__(self, *args, **kwargs):

        for field in self._meta.fields:
            val = field.get_default()

            if kwargs:
                if isinstance(field, BaseRelationField):
                    related_model_class = field.get_related_model_class()

                    if field.name in kwargs:
                        val = kwargs.pop(field.name)
                    else:
                        val = related_model_class.from_api({
                            field.remote_field.name: kwargs.pop(field.attname)
                        }, self._meta.swapi_client, True)

                elif field.name in kwargs:
                    val = kwargs.pop(field.name)

            if field.null and field.attname in kwargs and kwargs.get(field.attname) is None:
                val = field.get_default()


            # self.add_to_class(field.name, field.clean(val))
            self.__dict__[field.name] = field.clean(val)
            # setattr(self, field.name, field.clean(val))
            self.concrete[field.name] = val

        super().__init__()

    @classmethod
    def from_api(cls, data, swapi_client, lazy=False):
        new = cls(**data)
        new._meta.use(swapi_client)

        if lazy:
            return LazyModel(model=cls, **data)
        return new

    def create(self, force=False):

        if force:
            changed_fields = self._meta.fields
        else:
            changed_fields = self._diff_fields()

        package = {
            field.attname: field.to_simple(getattr(self, field.name)) for field in changed_fields if
            field.read_only is False
        }

        self._meta.swapi_client.post(url={
            "model": (self._meta.api_endpoint)
        }, data=json.dumps(package))

    def delete(self):
        self._meta.swapi_client.delete(url={
            "model": (self._meta.api_endpoint, self._get_pk_val().hex)
        })

    def update(self, force=False):

        if force:
            changed_fields = self._meta.fields
        else:
            changed_fields = self._diff_fields()

        package = {
            field.attname: field.to_simple(getattr(self, field.name)) for field in changed_fields if
            field.read_only is False
        }

        if self._meta.pk.attname in self._meta.pk.attname:
            pk_val = package[self._meta.pk.attname]

        self._meta.swapi_client.patch(url={
            "model": (self._meta.api_endpoint, pk_val)
        }, data=json.dumps(package))

    def _diff_fields(self):
        diff_field_list = []
        for field in self._meta.fields:
            if getattr(self, field.name) != self.concrete[field.name]:
                diff_field_list.append(field)
        return diff_field_list

    def _get_pk_val(self, meta=None):
        meta = meta or self._meta
        return getattr(self, meta.pk.attname)

    # def _set_pk_val(self, value):
    #     for parent_link in self._meta.parents.values():
    #         if parent_link and parent_link != self._meta.pk:
    #             setattr(self, parent_link.target_field.attname, value)
    #     return setattr(self, self._meta.pk.attname, value)

    # pk = property(_get_pk_val, _set_pk_val)

    def reverse(self, name):
        for r in self._reverse:
            if name == r.model._meta.model.__name__:
                return r.model.objects.use(self._meta.swapi_client).filter(**{r.related_name: self._get_pk_val()} )


class LazyModel:

    def __init__(self, *args, model=None, **kwargs):
        self._model = model
        self._kwargs = kwargs
        self._converted = False
        name = model._meta.pk.name

        setattr(self, name, self._kwargs.get(name))

    def _get_pk_val(self, meta=None):
        return getattr(self, self.model._meta.pk.name)

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
