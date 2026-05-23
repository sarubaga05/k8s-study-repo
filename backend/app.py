import os
import redis
import psycopg2
from flask import Flask, request, jsonify, redirect
from prometheus_client import Counter, generate_latest, REGISTRY
import time

app = Flask(__name__)

# Prometheus метрики
VOTE_COUNTER = Counter('votes_total', 'Total votes', ['choice'])

# Подключения к БД
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis-service'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres-service'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'voting'),
        user=os.getenv('DB_USER', 'voting_user'),
        password=os.getenv('DB_PASSWORD', 'voting_pass')
    )

# Инициализация БД
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL PRIMARY KEY,
            choice VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/ready')
def ready():
    # Проверяем связь с БД и Redis
    try:
        conn = get_db_connection()
        conn.close()
        redis_client.ping()
        return {'status': 'ready'}, 200
    except Exception as e:
        return {'status': 'not ready', 'error': str(e)}, 500

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.json.get('choice')
    if choice not in ['cat', 'dog']:
        return {'error': 'Invalid choice'}, 400
    
    # Пишем в Redis (кэш)
    redis_client.hincrby('votes', choice, 1)
    
    # Пишем в PostgreSQL (персистентность)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO votes (choice) VALUES (%s)', (choice,))
    conn.commit()
    cur.close()
    conn.close()
    
    # Обновляем метрику
    VOTE_COUNTER.labels(choice=choice).inc()
    
    return {'status': 'voted', 'choice': choice}, 201

@app.route('/results')
def results():
    # Сначала пробуем из Redis (быстро)
    redis_results = redis_client.hgetall('votes')
    
    # Для точности берем из БД общее количество
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT choice, COUNT(*) FROM votes GROUP BY choice')
    db_results = dict(cur.fetchall())
    cur.close()
    conn.close()
    
    # Мерджим результаты
    cats = db_results.get('cat', 0)
    dogs = db_results.get('dog', 0)
    
    return jsonify({
        'cat': cats,
        'dog': dogs,
        'total': cats + dogs,
        'cache_hit': bool(redis_results)
    })

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)