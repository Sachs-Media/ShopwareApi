=============
Configuration
=============

To access the configuration, use the following code

.. code-block:: python

    from shopwareapi.utils.conf import settings

    print(settings.TOKEN_EXPIRE_RENEW_THRESHOLD)

All Configuration Parameters are UPPERCASE

.. code-block:: python

    from shopwareapi.client import ShopwareClient

    client = ShopwareClient(base_url="http://localhost")
    print(client.BASE_URL)


.. autoclass:: shopwareapi.utils.conf.DefaultConfiguration
   :private-members:
   :members:

.. _shopwareapi-utils-conf-configuration:

.. autoclass:: shopwareapi.utils.conf.Configuration
   :private-members:
   :members:
   :special-members: __setattr__

