import redis
import os
import json
import time
import logging

# Configuraciones desde .env
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = int(os.getenv("CACHE_TTL", 60))  # TTL en segundos

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cache")

# Conectar a Redis con reintentos automáticos
def connect_redis(retries=5, delay=2):
    for attempt in range(retries):
        try:
            client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            client.ping()
            logger.info("✅ Connected to Redis")
            return client
        except redis.exceptions.ConnectionError as e:
            logger.warning(f"⚠️ Redis connection failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    logger.error("❌ Failed to connect to Redis after retries.")
    return None

# Cliente global
redis_client = connect_redis()

# Generar clave única para cada feed por usuario y página
def _generate_key(user_id: str, page: int) -> str:
    return f"feed:{user_id}:{page}"

# Obtener del cache
def get_cached_feed(user_id: str, page: int):
    if not redis_client:
        logger.warning("❌ Redis not available. Skipping cache get.")
        return None

    try:
        key = _generate_key(user_id, page)
        cached = redis_client.get(key)
        if cached:
            logger.debug(f"📥 Cache hit for key: {key}")
        else:
            logger.debug(f"📭 Cache miss for key: {key}")
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.warning(f"⚠️ Error getting cached feed: {e}")
        return None

# Guardar en cache
def set_cached_feed(user_id: str, page: int, data):
    if not redis_client:
        logger.warning("❌ Redis not available. Skipping cache set.")
        return

    try:
        key = _generate_key(user_id, page)
        redis_client.setex(key, CACHE_TTL, json.dumps(data))
        logger.debug(f"📤 Cache set for key: {key} (TTL: {CACHE_TTL}s)")
    except Exception as e:
        logger.warning(f"⚠️ Error setting cached feed: {e}")
