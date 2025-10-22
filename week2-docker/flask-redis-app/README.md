# Flask + Redis Multi-Container Application

## Overview
A visitor counter web application demonstrating Docker multi-container architecture with manual container orchestration.

## Architecture
```
User → Port 5000 → Flask Container → Docker Network → Redis Container
                        ↓
                   Stores visit count
```

## Components

### 1. Flask Web Application
- Python web server using Flask framework
- Handles HTTP requests on port 5000
- Connects to Redis to increment visit counter
- Displays visit count to users

### 2. Redis Cache
- In-memory data store
- Stores visit counter as key-value pair
- Provides fast read/write operations
- Runs on internal port 6379 (not exposed externally)

### 3. Docker Network
- Custom bridge network `flask-net`
- Enables container-to-container communication
- Provides DNS resolution (Flask finds Redis by name)

## Project Files
```
flask-redis-app/
├── app.py              # Flask application code
├── requirements.txt    # Python dependencies
├── Dockerfile         # Instructions to build Flask image
└── README.md          # This file
```

## How It Works

### Container Communication
1. Both containers connect to custom network `flask-net`
2. Flask container references Redis as `redis:6379` (service name)
3. Docker's internal DNS resolves `redis` to Redis container's IP
4. No hard-coded IP addresses needed

### Request Flow
1. User sends HTTP request to `http://localhost:5000`
2. Host machine forwards request to Flask container port 5000
3. Flask app calls `cache.incr('visits')` to increment counter
4. Redis increments counter and returns new value
5. Flask renders HTML response with counter
6. Response sent back to user

### Data Storage
- Redis stores counter in memory (not persistent in this version)
- Counter resets when Redis container is removed
- Data survives container restart (not removal)

## Setup and Running

### Prerequisites
- Docker installed
- Port 5000 available on host machine

### Build and Run
```bash
# 1. Create Docker network
docker network create flask-net

# 2. Start Redis container
docker run -d \
  --name redis \
  --network flask-net \
  redis:alpine

# 3. Build Flask application image
docker build -t flask-app .

# 4. Start Flask container
docker run -d \
  --name web \
  --network flask-net \
  -p 5000:5000 \
  flask-app
```

### Verify Running
```bash
# Check both containers are running
docker ps

# Should show:
# CONTAINER ID   IMAGE          COMMAND           STATUS        PORTS
# <id>           flask-app      "python app.py"   Up 2 min      0.0.0.0:5000->5000/tcp
# <id>           redis:alpine   "redis-server"    Up 3 min      6379/tcp
```

### Test Application
```bash
# Test the application
curl localhost:5000

# Or open in browser
http://localhost:5000

# Test multiple times to see counter increment
curl localhost:5000  # Visit 1
curl localhost:5000  # Visit 2
curl localhost:5000  # Visit 3
```

## Management Commands

### View Logs
```bash
# Flask application logs
docker logs web
docker logs -f web  # Follow logs in real-time

# Redis logs
docker logs redis
docker logs -f redis
```

### Execute Commands in Containers
```bash
# Open shell in Flask container
docker exec -it web bash

# Check Redis data directly
docker exec redis redis-cli GET visits

# View Redis info
docker exec redis redis-cli INFO
```

### Stop and Remove
```bash
# Stop containers
docker stop web redis

# Remove containers
docker rm web redis

# Remove network
docker network rm flask-net

# Remove image
docker rmi flask-app
```

### Complete Cleanup
```bash
# One-liner to stop and remove everything
docker stop web redis && docker rm web redis && docker network rm flask-net
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Stop conflicting container
docker stop <container-name>

# Or use different port
docker run -d --name web --network flask-net -p 5001:5000 flask-app
```

### Flask Cannot Connect to Redis
```bash
# Check both containers are on same network
docker network inspect flask-net

# Check Redis is running
docker ps | grep redis

# Check Redis logs for errors
docker logs redis

# Verify Flask can reach Redis
docker exec web ping redis
```

### Container Keeps Restarting
```bash
# Check logs for errors
docker logs web

# Common issues:
# - Missing dependencies in requirements.txt
# - Syntax errors in app.py
# - Redis not available when Flask starts
```

### Reset Everything
```bash
# Complete cleanup and restart
docker stop web redis
docker rm web redis
docker network rm flask-net
docker network create flask-net

# Rebuild and restart
docker build -t flask-app .
docker run -d --name redis --network flask-net redis:alpine
docker run -d --name web --network flask-net -p 5000:5000 flask-app
```

## Code Explanation

### app.py
```python
from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis using service name 'redis'
# Docker's DNS resolves this to Redis container's IP
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    # Increment counter in Redis (atomic operation)
    visits = cache.incr('visits')
    return f'Page visited {visits} times'

if __name__ == '__main__':
    # Listen on all interfaces so Docker can forward traffic
    app.run(host='0.0.0.0', port=5000)
```

**Key points:**
- `host='redis'` - Uses Docker's service discovery
- `cache.incr('visits')` - Atomic increment operation
- `host='0.0.0.0'` - Required for Docker port mapping

### Dockerfile
```dockerfile
FROM python:3.9-slim          # Lightweight Python base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependencies first (caching)
RUN pip install --no-cache-dir -r requirements.txt  # Install packages
COPY app.py .                  # Copy application code
EXPOSE 5000                    # Document exposed port
CMD ["python", "app.py"]       # Run application
```

**Why this order?**
- Dependencies copied before code for better Docker layer caching
- If code changes, only last layers rebuild
- If dependencies change, everything after rebuilds

## Key Concepts Learned

### 1. Container Networking
- Custom bridge networks enable inter-container communication
- Service discovery via DNS (container name = hostname)
- Network isolation from host machine

### 2. Multi-Container Applications
- Different services in separate containers
- Containers communicate over Docker network
- Each container has single responsibility

### 3. Port Mapping
- `-p host:container` maps ports
- Only Flask needs external access (port 5000)
- Redis is internal only (more secure)

### 4. Service Dependencies
- Application containers depend on data stores
- Must start services in correct order
- Handle connection failures gracefully

### 5. Container Lifecycle
- Containers are ephemeral (temporary)
- Data in containers is lost when removed
- Use volumes for persistent data (future enhancement)

## Comparison: Manual vs Docker Compose

### Manual Approach (What We Did)
```bash
docker network create flask-net
docker run -d --name redis --network flask-net redis:alpine
docker build -t flask-app .
docker run -d --name web --network flask-net -p 5000:5000 flask-app
```

**Pros:**
- Full control over each step
- Understand what's happening
- No additional tools needed

**Cons:**
- Multiple commands to remember
- Harder to reproduce
- No service restart policies
- Manual dependency management

### Docker Compose Approach (Future)
```yaml
services:
  web:
    build: .
    ports: ["5000:5000"]
    depends_on: [redis]
  redis:
    image: redis:alpine
```
```bash
docker-compose up -d  # Start everything
```

**Pros:**
- Single command
- Declarative configuration
- Automatic network creation
- Built-in restart policies
- Easy to share and reproduce

## Real-World Applications

This pattern is used in production for:
- **E-commerce sites:** Web app + Redis session store + PostgreSQL
- **Social media:** API server + Redis cache + Message queue
- **Analytics:** Data processor + Redis + Time-series database
- **Microservices:** Multiple APIs + Shared cache + Service mesh

## Next Steps

### Enhancements to Try

1. **Add data persistence:**
```bash
   docker run -d --name redis --network flask-net \
     -v redis-data:/data \
     redis:alpine redis-server --appendonly yes
```

2. **Add environment variables:**
```bash
   docker run -d --name web --network flask-net \
     -e REDIS_HOST=redis \
     -e REDIS_PORT=6379 \
     -p 5000:5000 flask-app
```

3. **Add health checks:**
```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost:5000/ || exit 1
```

4. **Add PostgreSQL database:**
```bash
   docker run -d --name postgres --network flask-net \
     -e POSTGRES_PASSWORD=secret \
     postgres:13-alpine
```

5. **Implement Docker Compose:**
   - Convert manual commands to `docker-compose.yml`
   - Use `docker compose up/down` for management
   - Add restart policies and health checks

## Learning Outcomes

✅ Built multi-container application from scratch  
✅ Created custom Docker networks  
✅ Implemented container-to-container communication  
✅ Used service discovery (DNS-based)  
✅ Managed container lifecycle manually  
✅ Debugged connection issues  
✅ Understood Docker networking architecture  
✅ Applied port mapping and network isolation  

## Resources

- [Docker Networking Documentation](https://docs.docker.com/network/)
- [Redis Documentation](https://redis.io/documentation)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Author Notes

**What worked well:**
- Manual approach helps understand fundamentals
- Custom network provides clean isolation
- Service discovery via DNS is elegant

**Challenges faced:**
- Docker Compose plugin not available on Amazon Linux 2023
- Required manual orchestration instead
- Understanding network creation was key

**Key takeaway:**
Understanding manual container orchestration makes Docker Compose usage more meaningful. When Compose automates these steps, you'll know exactly what it's doing under the hood.
