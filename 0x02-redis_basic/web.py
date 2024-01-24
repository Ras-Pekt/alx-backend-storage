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
    content = f"content:{url}"
    counter = f"count:{url}"
    cache.incr(counter)

    data = cache.get(content)
    if data:
        return data.decode("utf-8")

    response = requests.get(url)
    new_content = response.text
    cache.setex(content, 10, new_content)
    return new_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
