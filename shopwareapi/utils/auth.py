import time

from shopwareapi.utils.conf import settings


def token_cache(func):
    """
        Cache decorator for Shopware HTTP-Authentification
        This method prevents requesting a accesstoken for every request
        the method manages the token, and fetches a new token before the expire_time has expired.
        The length of time before the expire time can be set using
        :attr:`shopwareapi.utils.conf.settings.TOKEN_EXPIRE_RENEW_THRESHOLD`

        .. seealso:: to learn more about :code:`TOKEN_EXPIRE_RENEW_THRESHOLD` visit :ref:`Configuration <shopwareapi-utils-conf-configuration>`

        :param func: Orginal Function
        :type func: function

        :return str: access_token
    """

    def wrapper(self, *args, **kwargs):
        if self._authorization is None or not self._authorization.get("t"):
            return func(self, *args, **kwargs)
        t = self._authorization.get("t")

        if time.time() - settings.TOKEN_EXPIRE_RENEW_THRESHOLD > t + self._authorization["response"].get("expire_in",
                                                                                                         0):
            return func(self, *args, **kwargs)
        else:
            return self._authorization["response"].get("access_token")

    return wrapper
