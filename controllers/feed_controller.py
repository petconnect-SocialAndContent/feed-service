from flask import Blueprint, request, jsonify
from services.feed_service import get_user_feed

feed_bp = Blueprint("feed", __name__)

@feed_bp.route("/<user_id>", methods=["GET"])
def get_feed(user_id):
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    feed = get_user_feed(user_id, page, limit)
    return jsonify(feed)
