from flask import Flask
import redis
import os

# Create Flask app
app = Flask(__name__)

# Connect to Redis
# 'redis' is the hostname (Docker Compose service name)
# Docker's internal DNS resolves 'redis' to the Redis container's IP
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    # Increment visit counter in Redis
    # Redis stores key-value pairs: 'visits' -> count
    visits = cache.incr('visits')
    
    return f'''
    <h1>Hello from Docker with Redis!</h1>
    <p>This page has been visited <strong>{visits}</strong> times</p>
    <p>Redis container is caching the visit count</p>
    <p>Refresh to see the counter increase!</p>
    '''

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) so Docker can forward requests
    app.run(host='0.0.0.0', port=5000)
