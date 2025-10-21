# Week 2: Docker Fundamentals

## Project 1: First Containerized Application

### What I Built
A simple Flask web application running in a Docker container.

### Environment
- AWS EC2 (Amazon Linux 2023)
- Docker installed and configured
- Python Flask app containerized

### Files
- `app.py` - Simple Flask web application
- `Dockerfile` - Container definition

### How to Build and Run
```bash
# Build the image
docker build -t my-first-app .

# Run the container
docker run -d -p 5000:5000 --name flask-app my-first-app

# Check logs
docker logs flask-app

# Test the app
curl localhost:5000

# Stop and remove
docker stop flask-app
docker rm flask-app
```

### What I Learned
- Docker image vs container concepts
- Writing a Dockerfile
- Building images with `docker build`
- Running containers with `docker run`
- Port mapping (-p flag)
- Container management (ps, logs, exec, stop, rm)
- Base images and layers

### Docker Commands Practiced
```bash
docker build      # Build image from Dockerfile
docker run        # Create and start container
docker ps         # List running containers
docker logs       # View container logs
docker exec       # Execute command in container
docker stop       # Stop running container
docker rm         # Remove container
docker images     # List images
```

## Next Steps
- Build multi-container application with docker-compose
- Add database container
- Learn Docker networking and volumes
