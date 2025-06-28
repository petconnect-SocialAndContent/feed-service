from models.post_model import get_posts_from_db
from utils.cache import get_cached_feed, set_cached_feed

def get_user_feed(user_id, page, limit):
    cached = get_cached_feed(user_id, page)
    if cached:
        return cached

    posts = get_posts_from_db(user_id, page, limit)
    set_cached_feed(user_id, page, posts)
    return posts
