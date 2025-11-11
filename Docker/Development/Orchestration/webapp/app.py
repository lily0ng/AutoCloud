from flask import Flask, jsonify
import redis
import psycopg2
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="appdb",
        user="user",
        password="password"
    )
    return conn

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def home():
    request_count.inc()
    return jsonify({"message": "Welcome to the orchestrated application!"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
