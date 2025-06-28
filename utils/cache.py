import redis
import os
import json

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)
CACHE_TTL = int(os.getenv("CACHE_TTL", 60))

def get_cached_feed(user_id, page):
    key = f"feed:{user_id}:page:{page}"
    data = r.get(key)
    return json.loads(data) if data else None

def set_cached_feed(user_id, page, feed):
    key = f"feed:{user_id}:page:{page}"
    r.setex(key, CACHE_TTL, json.dumps(feed))
