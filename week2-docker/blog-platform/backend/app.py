from flask import Flask, request, jsonify, session
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import os
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-in-prod')

# CORS Configuration
CORS(app, supports_credentials=True, origins=['*'])

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'database': os.getenv('POSTGRES_DB', 'blogdb'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'secret')
}

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Helper Functions
def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()

def verify_password(stored_password, provided_password):
    """Verify hashed password"""
    salt = stored_password[:64]
    stored_hash = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

def login_required(f):
    """Login required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        cache.ping()
        
        # Calculate cache stats
        cache_hits = int(cache.get('cache_hits') or 0)
        cache_misses = int(cache.get('cache_misses') or 0)
        total = cache_hits + cache_misses
        hit_rate = f"{(cache_hits / total * 100):.1f}%" if total > 0 else "0%"
        
        return jsonify({
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok',
            'cache_hit_rate': hit_rate
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM users")
        users_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) FROM posts")
        posts_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) FROM comments")
        comments_count = cur.fetchone()['count']
        
        cur.execute("SELECT COALESCE(SUM(views), 0) FROM posts")
        total_views = cur.fetchone()['coalesce']
        
        cur.close()
        conn.close()
        
        return jsonify({
            'users': users_count,
            'posts': posts_count,
            'comments': comments_count,
            'total_views': int(total_views)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({'error': 'Username must be 3-20 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id, username, email",
                (username, email, hashed_password)
            )
            user = cur.fetchone()
            conn.commit()
            
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            cur.close()
            conn.close()
            
            return jsonify({
                'message': 'Registration successful',
                'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
            }), 201
        except psycopg2.IntegrityError:
            conn.rollback()
            return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            return jsonify({
                'message': 'Login successful',
                'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user info"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, username, email, bio, created_at FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user:
            return jsonify(dict(user)), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        category = request.args.get('category', '')
        search = request.args.get('search', '')
        
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT p.id, p.title, p.content, p.views, p.likes, p.created_at, p.category,
                   u.username as author
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (p.title ILIKE %s OR p.content ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if category:
            query += " AND p.category = %s"
            params.append(category)
        
        query += " ORDER BY p.created_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        
        cur.execute(query, params)
        posts = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([dict(post) for post in posts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post with comments"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Increment views
        cur.execute("UPDATE posts SET views = views + 1 WHERE id = %s", (post_id,))
        conn.commit()
        
        # Get post
        cur.execute("""
            SELECT p.*, u.username as author
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.id = %s
        """, (post_id,))
        post = cur.fetchone()
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Get comments
        cur.execute("""
            SELECT c.*, u.username as author
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at DESC
        """, (post_id,))
        comments = cur.fetchall()
        
        cur.close()
        conn.close()
        
        post_dict = dict(post)
        post_dict['comments'] = [dict(comment) for comment in comments]
        
        return jsonify(post_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['POST'])
@login_required
def create_post():
    """Create new post"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'General').strip()
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO posts (title, content, author_id, category)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, content, views, likes, created_at, category
        """, (title, content, session['user_id'], category))
        
        post = cur.fetchone()
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify(dict(post)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add comment to post"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Comment content required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO comments (post_id, user_id, content)
            VALUES (%s, %s, %s)
            RETURNING id, content, created_at
        """, (post_id, session['user_id'], content))
        
        comment = cur.fetchone()
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify(dict(comment)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """Like/Unlike a post"""
    try:
        user_id = session['user_id']
        cache_key = f"like:{user_id}:{post_id}"
        
        liked = cache.get(cache_key)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        if liked:
            cur.execute("UPDATE posts SET likes = likes - 1 WHERE id = %s", (post_id,))
            cache.delete(cache_key)
            action = 'unliked'
        else:
            cur.execute("UPDATE posts SET likes = likes + 1 WHERE id = %s", (post_id,))
            cache.set(cache_key, '1', ex=86400*30)
            action = 'liked'
        
        conn.commit()
        
        cur.execute("SELECT likes FROM posts WHERE id = %s", (post_id,))
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return jsonify({'action': action, 'likes': result['likes']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories with post counts"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT category, COUNT(*) as count
            FROM posts
            GROUP BY category
            ORDER BY count DESC
        """)
        
        categories = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([dict(cat) for cat in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
