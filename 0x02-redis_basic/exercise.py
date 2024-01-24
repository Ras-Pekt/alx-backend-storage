#!/usr/bin/env python3
"""
a Cache class module
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    deocrator to calculate number of method calls
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    a decorator that stores the history of inputs and outputs
    for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        """
        uniq_id = str(uuid.uuid4())
        self._redis.set(uniq_id, data)
        return uniq_id

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """
        converts the data back to the desired format
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get
        """
        return self.get(key, fn=int)

    def replay(self, method: Callable) -> None:
        """
        display the history of calls of a particular function.
        """
        method_name = method.__qualname__
        inputs = self._redis.lrange(f"{method_name}:inputs", 0, -1)
        outputs = self._redis.lrange(f"{method_name}:outputs", 0, -1)

        print(f"{method_name} was called {len(list(inputs))} times:")
        io_list = list(zip(inputs, outputs))
        for input, output in io_list:
            input = input.decode('utf8')
            output = output.decode('utf8')
            print(f"{method_name}(*{input}) -> {output}")
