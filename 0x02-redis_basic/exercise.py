#!/usr/bin/env python3
"""
a Cache class module
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    a Cache class that instantiates Redis client and flushes the instance,
    with a method that takes a data argument and returns a string.
    """
    def __init__(self):
        """
        initiliazation function
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        """
        uniq_id = str(uuid.uuid4())
        self._redis.set(uniq_id, data)
        return uniq_id

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """
        takes a key string argument and an optional Callable argument
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """
        automatically parametrize Cache.get
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        automatically parametrize Cache.get
        """
        return self.get(key, fn=int)
