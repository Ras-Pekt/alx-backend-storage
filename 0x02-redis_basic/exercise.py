#!/usr/bin/env python3
"""
a Cache class module
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    a Cache class that instantiates Redis client and flushes the instance,
    with a method that takes a data argument and returns a string.
    """
    def __init__(self) -> None:
        """
        initiliazation function
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, bytes, float, str]) -> str:
        """
        takes a data argument and returns a string
        """
        uniq_id = str(uuid.uuid4())
        self._redis.set(uniq_id, data)
        return uniq_id
