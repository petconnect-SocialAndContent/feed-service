# utils/metrics.py
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
import time

# Contadores
REQUEST_COUNT = Counter(
    'feed_requests_total', 'Total HTTP requests to the feed service',
    ['method', 'endpoint', 'http_status']
)

# Tiempo de respuesta
REQUEST_LATENCY = Histogram(
    'feed_request_duration_seconds', 'Latency of feed requests in seconds',
    ['endpoint']
)

# Middleware de monitoreo
def monitor(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_metrics(response):
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.path).observe(latency)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
        return response

# Endpoint de métricas
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
