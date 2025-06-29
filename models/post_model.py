from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client["feeddb"]
posts_collection = db["posts"]

def get_posts_from_db(user_id, page, limit):
    try:
        page = int(page)
        limit = int(limit)
        skip = (page - 1) * limit

        # Convertir user_id a ObjectId si corresponde
        if ObjectId.is_valid(user_id):
            query = {"user_id": ObjectId(user_id)}
        else:
            query = {"user_id": user_id}

        posts = list(posts_collection.find(query).sort("created_at", -1).skip(skip).limit(limit))
        for post in posts:
            post["_id"] = str(post["_id"])
        return posts
    except Exception as e:
        print("Mongo query error:", e)
        return []
