from flask import Flask, render_template_string, request, redirect
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = Flask(__name__)

# Connect to Redis (cache layer)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

# PostgreSQL connection function
def get_db_connection():
    """
    Connect to PostgreSQL database.
    Uses environment variables for configuration (12-factor app principle).
    """
    return psycopg2.connect(
        host='postgres',
        database=os.getenv('POSTGRES_DB', 'guestbook'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'secret'),
        cursor_factory=RealDictCursor  # Returns results as dictionaries
    )

# HTML template (embedded for simplicity)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Guestbook</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .stats {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        form {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .visitor {
            background: #fff;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #4CAF50;
            border-radius: 4px;
        }
        .visitor-name {
            font-weight: bold;
            color: #333;
        }
        .visitor-time {
            color: #666;
            font-size: 0.9em;
        }
        .cache-indicator {
            display: inline-block;
            padding: 3px 8px;
            background: #ff9800;
            color: white;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Docker Guestbook</h1>
        
        <div class="stats">
            <strong>📊 Statistics:</strong><br>
            Total Visitors: {{ total_visitors }}<br>
            Cache Hit Rate: {{ cache_hits }}%<br>
            Page Views: {{ page_views }}
        </div>

        <h2>✍️ Sign the Guestbook</h2>
        <form method="POST" action="/sign">
            <input type="text" name="name" placeholder="Your Name" required>
            <textarea name="message" placeholder="Your Message" rows="3" required></textarea>
            <button type="submit">Sign Guestbook</button>
        </form>

        <h2>👥 Recent Visitors</h2>
        {% for visitor in visitors %}
        <div class="visitor">
            <div class="visitor-name">
                {{ visitor.name }}
                {% if visitor.from_cache %}
                <span class="cache-indicator">CACHED</span>
                {% endif %}
            </div>
            <div>{{ visitor.message }}</div>
            <div class="visitor-time">{{ visitor.timestamp }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """
    Main page - shows guestbook entries.
    Demonstrates cache-aside pattern: check cache first, then database.
    """
    # Increment page view counter in Redis
    page_views = cache.incr('page_views')
    
    # Try to get recent visitors from cache first (cache-aside pattern)
    cached_visitors = cache.get('recent_visitors')
    
    if cached_visitors:
        # Cache hit! Use cached data
        cache.incr('cache_hits')
        visitors = eval(cached_visitors)  # In production, use json.loads()
        for v in visitors:
            v['from_cache'] = True
    else:
        # Cache miss - query database
        cache.incr('cache_misses')
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get 10 most recent visitors
        cur.execute('''
            SELECT name, message, timestamp 
            FROM visitors 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        visitors = cur.fetchall()
        
        # Store in cache for 60 seconds
        cache.setex('recent_visitors', 60, str(visitors))
        
        for v in visitors:
            v['from_cache'] = False
            
        cur.close()
        conn.close()
    
    # Get total visitor count from database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as count FROM visitors')
    total_visitors = cur.fetchone()['count']
    cur.close()
    conn.close()
    
    # Calculate cache hit rate
    cache_hits = int(cache.get('cache_hits') or 0)
    cache_misses = int(cache.get('cache_misses') or 0)
    total_requests = cache_hits + cache_misses
    cache_hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
    
    return render_template_string(
        HTML_TEMPLATE,
        visitors=visitors,
        total_visitors=total_visitors,
        page_views=page_views,
        cache_hits=f"{cache_hit_rate:.1f}"
    )

@app.route('/sign', methods=['POST'])
def sign():
    """
    Handle guestbook signing.
    Writes to database and invalidates cache.
    """
    name = request.form.get('name')
    message = request.form.get('message')
    
    # Insert into PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO visitors (name, message) VALUES (%s, %s)',
        (name, message)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    # Invalidate cache so next request gets fresh data
    cache.delete('recent_visitors')
    
    return redirect('/')

@app.route('/health')
def health():
    """
    Health check endpoint.
    Verifies connections to Redis and PostgreSQL.
    """
    try:
        # Check Redis
        cache.ping()
        
        # Check PostgreSQL
        conn = get_db_connection()
        conn.close()
        
        return {'status': 'healthy', 'redis': 'ok', 'postgres': 'ok'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
