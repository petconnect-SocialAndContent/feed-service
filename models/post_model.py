import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
db = client["feeddb"]
posts_collection = db["posts"]

def get_posts_from_db(user_id, page, limit):
    skip = (page - 1) * limit
    return list(posts_collection.find().sort("created_at", -1).skip(skip).limit(limit))
