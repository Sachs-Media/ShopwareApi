=============
Configuration
=============

To access the configuration, use the following code

.. code-block:: python

    from shopwareapi.utils.conf import settings

    print(settings.TOKEN_EXPIRE_RENEW_THRESHOLD)


.. autoclass:: shopwareapi.utils.conf.DefaultConfiguration
   :private-members:
   :members:

.. autoclass:: shopwareapi.utils.conf.Configuration
   :private-members:
   :members:
   :special-members: __setattr__

