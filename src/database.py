import pymongo


def connect_to_mongo():
    username = "root"
    password = "rootpassword"
    client = pymongo.MongoClient("mongodb://localhost:27017/", username=username, password=password)
    database = client["Tarkov-app-db"]
    return database


def get_collections(database):
    items_collection = database["Items"]
    mapping_collection = database["mapping"]
    downloads_collection = database["downloads"]
    quests_collection = database["quests"]
    return items_collection, mapping_collection, downloads_collection, quests_collection
