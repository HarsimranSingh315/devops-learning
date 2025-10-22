# Production Deployment Guide

## Security Features

✅ **Multi-stage builds** - 3x smaller images  
✅ **Non-root user** - Runs as `appuser`  
✅ **Read-only filesystem** - Prevents malware  
✅ **Resource limits** - CPU and memory constraints  
✅ **Vulnerability scanning** - Trivy integration  
✅ **Secrets management** - No hardcoded passwords  

## Resource Allocation

| Service | CPU | Memory | Storage |
|---------|-----|--------|---------|
| PostgreSQL | 1.0 core | 512MB | Volume |
| Redis | 0.5 core | 128MB | Memory |
| Flask | 0.5 core | 256MB | None |

## Quick Start
```bash
./deploy-production.sh
```

## Monitoring
```bash
./monitor.sh
```

## Backup
```bash
# Backup database
docker exec postgres pg_dump -U postgres guestbook > backup.sql

# Backup volume
docker run --rm -v postgres-prod-data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/postgres-backup.tar.gz /data
```

## Rollback
```bash
docker stop web
docker run -d ... flask-app:previous-version
```

## Troubleshooting

See logs:
```bash
docker logs -f web
docker logs -f postgres
docker logs -f redis
```

## Security Scan
```bash
trivy image flask-app:production
```
