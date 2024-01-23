#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs stored in MongoDB
"""

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017")
    logs = client.logs
    collections = logs.nginx

    print(f"{collections.count_documents({})} logs\nMethods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collections.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    count = collections.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{count} status check")

    ip_logs = collections.aggregate(
        [
            {"$group": {"_id": "$ip", "total_requests": {"$sum": 1}}},
            {"$sort": {"total_requests": -1}},
            {"$limit": 10}
        ]
    )
    print("IPs:")
    for log in ip_logs:
        print(f'\t{log.get("_id")}: {log.get("total_requests")}')
