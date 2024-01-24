#!/usr/bin/env python3
"""
a function that uses the requests module
to obtain the HTML content of a particular URL and returns it
"""
import requests
import redis

cache = redis.Redis()


def get_page(url: str) -> str:
    """
    takes a url and returns the contents of the url
    """
    content_key = "html:{}".format(url)
    counter_key = "count:{}".format(url)
    cache.incr(counter_key)

    data = cache.get(content_key)
    if data:
        return data.decode("utf-8")

    response = requests.get(url)
    fresh_content = response.text
    cache.set(content_key, fresh_content, ex=10)
    return fresh_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
