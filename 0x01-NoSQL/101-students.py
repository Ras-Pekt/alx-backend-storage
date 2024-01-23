#!/usr/bin/env python3
"""
a function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """
    students = mongo_collection.aggregate(
        [
            {
                "$project": {
                    "name": 1,
                    "averageScore": {
                        "$avg": "$topics.score"
                    },
                    "topics": 1
                }
            },
            {
                "$sort": {
                    "averageScore": -1
                }
            }
        ]
    )
    return students
