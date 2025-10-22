# Production Blog Platform

## Overview
A complete, production-ready blog platform demonstrating modern microservices architecture with reverse proxy, API backend, caching, and persistent storage.

## Architecture
```
                    Internet (Port 80)
                           ↓
                    [Nginx Reverse Proxy]
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                                     ↓
   [Frontend:3000]                      [Backend API:5000]
   Static HTML/CSS/JS                   Flask REST API
        ↓                                     ↓
        └──────────────────┬──────────────────┘
                           ↓
                   ┌───────┴────────┐
                   ↓                ↓
              [Redis Cache]    [PostgreSQL]
              Session Store    Persistent DB
```

## Technology Stack

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Modern CSS with gradients and animations
- Responsive design
- Modal-based UI

**Backend:**
- Flask 3.0 (Python web framework)
- Flask-CORS (Cross-origin requests)
- RESTful API design
- Session-based authentication

**Database:**
- PostgreSQL 13 (Relational database)
- UUID primary keys
- Foreign key relationships
- Indexed queries

**Cache:**
- Redis Alpine (In-memory cache)
- Session storage
- Cache-aside pattern

**Infrastructure:**
- Nginx (Reverse proxy & load balancer)
- Docker containers
- Bridge networking
- Volume persistence

## Features

### User Features
✅ User registration and authentication  
✅ Create, read, update, delete blog posts  
✅ Add comments to posts  
✅ View post statistics (views, comments)  
✅ Real-time platform statistics  
✅ Session management  

### Technical Features
✅ RESTful API architecture  
✅ JWT-free session authentication  
✅ Database persistence with PostgreSQL  
✅ Redis caching for performance  
✅ Nginx reverse proxy  
✅ Health check endpoints  
✅ CORS enabled  
✅ SQL injection protection (parameterized queries)  
✅ Cascade deletes (referential integrity)  

## Project Structure
```
blog-platform/
├── backend/
│   ├── app.py              # Flask API (11,925 bytes)
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container image
├── frontend/
│   ├── index.html          # Single-page application
│   ├── nginx.conf          # Frontend server config
│   └── Dockerfile          # Frontend container image
├── nginx/
│   ├── nginx.conf          # Reverse proxy config
│   └── Dockerfile          # Nginx container image
├── init-db.sql             # Database schema & seed data
├── docker-compose.yml      # Container orchestration
└── README.md               # This file
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Posts Table
```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    views INTEGER DEFAULT 0
);
```

### Comments Table
```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/me` - Get current user

### Posts (CRUD)
- `GET /api/posts` - List all posts (cached)
- `GET /api/posts/:id` - Get single post
- `POST /api/posts` - Create post (auth required)
- `PUT /api/posts/:id` - Update post (author only)
- `DELETE /api/posts/:id` - Delete post (author only)

### Comments
- `POST /api/posts/:id/comments` - Add comment (auth required)

### System
- `GET /api/health` - Health check
- `GET /api/stats` - Platform statistics

## Deployment

### Quick Start (Manual)
```bash
# Create network
docker network create blog-network

# Start PostgreSQL
docker run -d \
  --name postgres \
  --network blog-network \
  -e POSTGRES_DB=blogdb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secret \
  -v $(pwd)/init-db.sql:/docker-entrypoint-initdb.d/init.sql \
  postgres:13-alpine

# Wait for database
sleep 10

# Start Redis
docker run -d \
  --name redis \
  --network blog-network \
  redis:alpine

# Build and start Backend
docker build -t blog-platform-backend ./backend
docker run -d \
  --name backend \
  --network blog-network \
  -e POSTGRES_HOST=postgres \
  -e POSTGRES_DB=blogdb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secret \
  -e REDIS_HOST=redis \
  blog-platform-backend

# Build and start Frontend
docker build -t blog-platform-frontend ./frontend
docker run -d \
  --name frontend \
  --network blog-network \
  blog-platform-frontend

# Build and start Nginx
docker build -t blog-platform-nginx ./nginx
docker run -d \
  --name nginx \
  --network blog-network \
  -p 80:80 \
  blog-platform-nginx
```

### Access Application
```
http://localhost            # Local development
http://YOUR_EC2_IP         # Production EC2
```

## Usage Examples

### Register User
```bash
curl -X POST http://localhost/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'
```

### Login
```bash
curl -X POST http://localhost/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"john","password":"pass123"}'
```

### Create Post
```bash
curl -X POST http://localhost/api/posts \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"My Post","content":"Post content here"}'
```

### Get Stats
```bash
curl http://localhost/api/stats
```

## Performance Optimization

### Caching Strategy
- Posts list cached for 60 seconds
- Cache invalidation on create/update/delete
- Session data stored in Redis

### Database Optimization
- Indexed columns: `author_id`, `created_at`, `post_id`
- Parameterized queries (SQL injection protection)
- Connection pooling ready

### Nginx Configuration
- Reverse proxy with upstream load balancing
- CORS headers enabled
- Health check endpoint

## Security Features

### Implemented
✅ Password hashing (SHA256)  
✅ Parameterized SQL queries  
✅ Session-based authentication  
✅ CORS configuration  
✅ Input validation  
✅ Cascade deletes  

### Production Recommendations
- Use bcrypt for password hashing
- Implement rate limiting
- Add HTTPS/TLS with Let's Encrypt
- Use environment variables for secrets
- Implement CSRF protection
- Add input sanitization
- Use prepared statements exclusively

## Monitoring

### Health Checks
```bash
# Application health
curl http://localhost/api/health

# Nginx health
curl http://localhost/health
```

### View Logs
```bash
docker logs backend
docker logs postgres
docker logs nginx
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U postgres -d blogdb

# View all posts
SELECT * FROM posts;

# View users
SELECT username, email, created_at FROM users;
```

## Troubleshooting

### Backend not starting
```bash
docker logs backend
# Check environment variables
# Verify PostgreSQL connection
```

### Frontend shows 502 error
```bash
docker logs nginx
# Verify frontend container is running
# Check nginx upstream configuration
```

### Database connection failed
```bash
docker exec postgres pg_isready -U postgres
# Verify network connectivity
docker network inspect blog-network
```

## Testing

### Manual Testing Workflow
1. Register a new user
2. Login with credentials
3. Create a blog post
4. View the post (verify view count increments)
5. Add a comment
6. Logout and verify authentication is required

### Load Testing
```bash
# Install Apache Bench
sudo yum install httpd-tools -y

# Test API performance
ab -n 1000 -c 10 http://localhost/api/posts
```

## Scaling Considerations

### Horizontal Scaling
- Add multiple backend replicas
- Use Redis for shared sessions
- Database read replicas
- Nginx load balancing

### Vertical Scaling
- Increase container resource limits
- Optimize database queries
- Increase connection pool sizes

## Lessons Learned

### Architecture Decisions
✅ Microservices provide clear separation of concerns  
✅ Reverse proxy enables easy scaling  
✅ Caching dramatically improves performance  
✅ Docker simplifies deployment  

### Challenges Overcome
- Docker Compose V2 compatibility issues
- Container networking configuration
- Frontend/backend port mapping
- Database initialization timing

### Best Practices Applied
- Health checks for all services
- Proper error handling
- RESTful API design
- Documentation-driven development

## Future Enhancements

- [ ] Add markdown support for posts
- [ ] Implement full-text search
- [ ] Add image upload capability
- [ ] Implement post categories/tags
- [ ] Add user profiles
- [ ] Email notifications
- [ ] Social sharing features
- [ ] Post drafts functionality
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Prometheus metrics
- [ ] Kubernetes deployment configs

## License
MIT License - Educational/Portfolio Project

## Author
Built as part of DevOps learning journey - Week 2, Day 5
Demonstrates: Docker, Microservices, REST APIs, Databases, Caching, Reverse Proxies

## Related Projects
- Week 2 Day 1: Single container applications
- Week 2 Day 2: Multi-container communication
- Week 2 Day 3: 3-tier architecture with caching
- Week 2 Day 4: Production optimization and security
- **Week 2 Day 5: Complete production platform** ← You are here
