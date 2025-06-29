from flask import Blueprint, request, jsonify
from services.feed_service import get_user_feed
from middleware.auth_middleware import jwt_required
import re

feed_bp = Blueprint('feed', __name__)

@feed_bp.route("/", methods=["GET"])
@jwt_required
def get_feed():
    """
    Obtener feed de publicaciones de un usuario
    ---
    tags:
      - Feed
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID del usuario (formato MongoDB ObjectId)
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Página del feed
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Número de elementos por página (máx 100)
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT en formato `Bearer <token>`
    responses:
      200:
        description: Lista de publicaciones del feed
        schema:
          type: array
          items:
            type: object
      400:
        description: Parámetros inválidos
      401:
        description: Token inválido o no enviado
      500:
        description: Error interno del servidor
    """
    try:
        user_id = request.args.get("user_id")
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        # Validaciones
        if not user_id or not re.match(r"^[a-fA-F0-9]{24}$", user_id):
            return jsonify({"error": "Invalid user_id"}), 400
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({"error": "Invalid pagination parameters"}), 400

        feed = get_user_feed(user_id, page, limit)
        return jsonify(feed)
    
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500
