#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

client = MongoClient()
db_logs = client["logs"]
db_collections = db_logs["nginx"]

print(f"{db_collections.count_documents({})} logs\nMethods:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

for method in methods:
    count = db_collections.count_documents({'method': method})
    print(f"\tmethod {method}: {count}")

count = db_collections.count_documents({'method': 'GET', 'path': '/status'})
print(f"{count} status check")
