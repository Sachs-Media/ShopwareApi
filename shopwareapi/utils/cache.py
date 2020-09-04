import time


def token_cache(func):
    def wrapper(self, *args, **kwargs):
        if self._authorization is None or not self._authorization.get("t"):
            return func(self, *args, **kwargs)
        t = self._authorization.get("t")

        if time.time()-60 > t+self._authorization["response"].get("expire_in", 0):
            return func(self, *args, **kwargs)
        else:
            return self._authorization["response"].get("access_token")
    return wrapper
