import os

from src.database import get_collections


group_items_by_id = {
    "$group": {
        "_id": "$name",
        "id": {
            "$first": "$id"
        },
        "count": {
            "$sum": 1
        }
    }
}

filter_count_gt_1 = {
    "$match": {
        "count": {
            "$gt": 1
        }
    }
}


def max_workers():
    return 2 * os.cpu_count() + 1


def remove_duplicates(database):
    items_collection, _, _ = get_collections(database)
    pipeline = [
        group_items_by_id,
        filter_count_gt_1
    ]
    for duplicated_item in items_collection.aggregate(pipeline):
        duplicated_id = duplicated_item["id"]
        any_item = items_collection.find_one({"id": duplicated_id})
        items_collection.delete_many({
            "_id": {
                "$ne": any_item["_id"]
            },
            "id": duplicated_id
        })
