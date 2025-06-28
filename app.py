from flask import Flask
from controllers.feed_controller import feed_bp
import os
from dotenv import load_dotenv
import redis

load_dotenv()

app = Flask(__name__)
app.register_blueprint(feed_bp, url_prefix="/api/feed")

# Conexión a Redis al iniciar
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    redis_client.ping()
    print("🟢 Connected to Redis")
except redis.exceptions.ConnectionError as e:
    print("🔴 Redis connection failed:", e)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3010))
    app.run(host="0.0.0.0", port=port)
