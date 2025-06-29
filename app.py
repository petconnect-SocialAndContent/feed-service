from flask import Flask
from controllers.feed_controller import feed_bp
from utils.cache import redis_client
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics
from flasgger import Swagger
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Configuración de Swagger
app.config['SWAGGER'] = {
    "title": "PetConnect Feed API",
    "uiversion": 3
}
swagger = Swagger(app)

# Prometheus para métricas
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Feed Service", version="1.0.0")

# Registrar rutas
app.register_blueprint(feed_bp, url_prefix="/api/feed")

# Endpoint de salud
@app.route("/health", methods=["GET"])
def health_check():
    try:
        redis_status = "connected" if redis_client.ping() else "not connected"
    except Exception:
        redis_status = "not connected"

    return {
        "status": "ok",
        "service": "feed-service",
        "redis": redis_status
    }, 200

# Ejecutar app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3010))
    app.run(host="0.0.0.0", port=port)
