-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) DEFAULT 'General',
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Insert sample users (password is "password123" for both)
-- Password hash format: salt(64 chars) + hash(64 chars)
INSERT INTO users (username, email, password, bio) VALUES
('johndoe', 'john@example.com', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd47d1ff60b75d5a4c1e0e7a52a38015f23f3eab1d80b931dd47d1ff60b75d5a4c1', 'DevOps Engineer | Docker Enthusiast'),
('janedoe', 'jane@example.com', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd47d1ff60b75d5a4c1e0e7a52a38015f23f3eab1d80b931dd47d1ff60b75d5a4c1', 'SRE | Kubernetes Expert')
ON CONFLICT (username) DO NOTHING;

-- Insert sample posts
INSERT INTO posts (title, content, author_id, category, views, likes)
VALUES
(
    'Getting Started with Docker',
    'Docker is a platform for developing, shipping, and running applications in containers.

Key Concepts:
- Images: Read-only templates for containers
- Containers: Running instances of images
- Dockerfile: Instructions to build images
- Docker Compose: Tool for multi-container apps

Why Docker?
✓ Consistency across environments
✓ Fast deployment
✓ Resource efficient
✓ Easy scaling

Docker has revolutionized how we deploy applications!',
    (SELECT id FROM users WHERE username = 'johndoe'),
    'Docker',
    150,
    12
),
(
    'Kubernetes Best Practices',
    'Production-ready Kubernetes requires careful planning.

Essential Practices:

1. Resource Management
   - Set resource requests and limits
   - Use horizontal pod autoscaling
   - Monitor resource usage

2. Health Checks
   - Liveness probes
   - Readiness probes
   - Startup probes

3. Security
   - Use RBAC
   - Network policies
   - Pod security standards
   - Secrets management

4. Observability
   - Centralized logging
   - Metrics collection
   - Distributed tracing
   - Alerting

Kubernetes is the standard for container orchestration!',
    (SELECT id FROM users WHERE username = 'janedoe'),
    'Kubernetes',
    230,
    18
),
(
    'Building Microservices Architecture',
    'Microservices architecture patterns for modern applications.

Key Patterns:

1. API Gateway
   - Single entry point
   - Request routing
   - Authentication

2. Service Discovery
   - Dynamic service location
   - Load balancing
   - Health checking

3. Circuit Breaker
   - Prevent cascading failures
   - Graceful degradation
   - Fast failure detection

4. Event-Driven
   - Async communication
   - Message queues
   - Event sourcing

Benefits:
✓ Independent deployment
✓ Technology flexibility
✓ Team autonomy
✓ Better scalability

Microservices offer great flexibility for large-scale applications!',
    (SELECT id FROM users WHERE username = 'johndoe'),
    'Microservices',
    180,
    15
)
ON CONFLICT DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
