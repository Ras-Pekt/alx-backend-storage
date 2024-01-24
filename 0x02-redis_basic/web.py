#!/usr/bin/env python3
"""
a function that uses the requests module
to obtain the HTML content of a particular URL and returns it
"""
import requests
import redis


def get_page(url: str) -> str:
    """
    takes a url and returns the contents of the url
    """
    cache = redis.Redis()
    cache.incr(f"count:{url}")

    data = cache.get(f"content:{url}")
    if data:
        return data.decode("utf-8")

    new_content = requests.get(url).text
    cache.setex(f"content:{url}", 10, new_content)
    return new_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
