import json

from shopwareapi.core.lazymodel import LazyModel
from shopwareapi.fields import ForeignKey, ManyToOneField
from shopwareapi.core.manager import Manager
from shopwareapi.core.query import QuerySet
from shopwareapi.core.options import Options
from shopwareapi.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from shopwareapi.utils.helper import has_contribute_to_class, subclass_exception
import logging


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
                if isinstance(field, ForeignKey):
                    related_model_class = field.get_related_model_class()

                    if field.name in kwargs:
                        val = kwargs.pop(field.name)
                    else:
                        if field.attname in kwargs:
                            val = related_model_class.from_api({
                                field.remote_field.name: kwargs.pop(field.attname)
                            }, self._meta.swapi_client, True)
                elif isinstance(field, ManyToOneField):
                    related_model_class = field.get_related_model_class()
                    vallist = []
                    if field.name in kwargs:
                        vallist = kwargs.pop(field.name)
                    elif field.attname in kwargs:
                        vallist = kwargs.pop(field.attname)
                    qs_pre = []
                    for data in vallist:
                        qs_pre.append(related_model_class.from_api(data, self._meta.swapi_client))
                    val = QuerySet(related_model_class, results=qs_pre)
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
            #field.attname: field.to_simple(getattr(self, field.name)) for field in changed_fields if
            #field.read_only is False
        }

        for field in changed_fields:
            if field.read_only is False:
                package[field.attname] = field.to_simple(getattr(self, field.name))

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
        self._meta.swapi_client.patch(url={
            "model": (self._meta.api_endpoint, self._get_pk_val().hex)
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


