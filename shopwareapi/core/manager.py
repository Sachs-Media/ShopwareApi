import inspect
from shopwareapi.client import ShopwareClient
from shopwareapi.core.query import QuerySet


class BaseManager:

    def __new__(cls, *args, **kwargs):
        # Capture the arguments to make returning them trivial.
        obj = super().__new__(cls)
        obj._constructor_args = (args, kwargs)
        return obj

    def __init__(self, **kwargs):
        self.model = None
        self.swapi_client = None
        self.name = None
        self._hints = {}
        super().__init__()

    def contribute_to_class(self, cls, name):
        self.name = self.name or name
        self.model = cls
        setattr(cls, name, ManagerDescriptor(self))
        cls._meta.set_manager(self)

    def use(self, swapi_client: ShopwareClient) -> "Manager":
        if isinstance(swapi_client, ShopwareClient):
            self.swapi_client = swapi_client
        else:
            ValueError("Client must be an instance of shopware.client.ShopwareClient class")
        return self

    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })

    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue

            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue

            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods

    def get_queryset(self):
        """
            Return a new QuerySet object. Subclasses can override this method to
            customize the behavior of the Manager.
        """
        return self._queryset_class(model=self.model, swapi_client=self.swapi_client)

    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):

            # Only copy missing methods.
            if hasattr(cls, name):
                continue

            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue

            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods


class Manager(BaseManager.from_queryset(QuerySet)):
    pass

class ManagerDescriptor:

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via %s instances" % cls.__name__)

        return cls._meta.local_manager
