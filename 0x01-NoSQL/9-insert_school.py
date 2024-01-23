#!/usr/bin/env python3
"""
a Python function that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection based on kwargs
    """
    # obj = mongo_collection.insert_one(dict(kwargs))
    return mongo_collection.insert_one(dict(kwargs)).inserted_id
