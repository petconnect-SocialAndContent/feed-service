import jwt
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.getenv("JWT_SECRET", "supersecreto123diegopetconnect456")

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"error": "Token not provided"}), 401
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded  # Puedes acceder luego con request.user["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function
