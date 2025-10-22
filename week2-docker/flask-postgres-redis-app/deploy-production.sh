#!/bin/bash
set -e

echo "🚀 Deploying Production Stack..."

# Configuration
NETWORK="flask-production"
POSTGRES_VOL="postgres-prod-data"
DB_PASSWORD="$(openssl rand -base64 32)"  # Generate secure password

# Cleanup old containers
echo "Cleaning up old containers..."
docker stop web postgres redis 2>/dev/null || true
docker rm web postgres redis 2>/dev/null || true

# Create network
echo "Creating network..."
docker network create ${NETWORK} 2>/dev/null || true

# Start PostgreSQL with resource limits
echo "Starting PostgreSQL..."
docker run -d \
  --name postgres \
  --network ${NETWORK} \
  --memory="512m" \
  --cpus="1.0" \
  --restart=unless-stopped \
  -e POSTGRES_PASSWORD=${DB_PASSWORD} \
  -e POSTGRES_DB=guestbook \
  -v ${POSTGRES_VOL}:/var/lib/postgresql/data \
  postgres:13-alpine

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
sleep 10

# Initialize database
echo "Initializing database..."
docker exec -i postgres psql -U postgres -d guestbook < init.sql

# Start Redis with resource limits
echo "Starting Redis..."
docker run -d \
  --name redis \
  --network ${NETWORK} \
  --memory="128m" \
  --cpus="0.5" \
  --restart=unless-stopped \
  redis:alpine

# Build optimized Alpine application
echo "Building application..."
docker build -t flask-app:alpine .

# Start Flask with security hardening
echo "Starting Flask application..."
docker run -d \
  --name web \
  --network ${NETWORK} \
  -p 5000:5000 \
  --memory="256m" \
  --cpus="0.5" \
  --read-only \
  --tmpfs /tmp \
  --restart=unless-stopped \
  -e POSTGRES_PASSWORD=${DB_PASSWORD} \
  -e POSTGRES_DB=guestbook \
  -e POSTGRES_USER=postgres \
  flask-app:alpine

echo "✅ Deployment complete!"
echo ""
echo "📊 Stack Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🔗 Access application: http://localhost:5000"
echo "💚 Health check: http://localhost:5000/health"

# Save password for reference
echo "${DB_PASSWORD}" > .db_password
chmod 600 .db_password
echo ""
echo "⚠️  Database password saved to .db_password (keep secure!)"
