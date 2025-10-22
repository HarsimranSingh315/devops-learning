#!/bin/bash

echo "📊 Container Health Status"
echo "=========================="
docker ps --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "💾 Resource Usage"
echo "================="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "🏥 Application Health"
echo "===================="
curl -s localhost:5000/health | python -m json.tool

echo ""
echo "📈 Cache Statistics"
echo "==================="
docker exec redis redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"

echo ""
echo "🗄️  Database Statistics"
echo "======================="
docker exec postgres psql -U postgres -d guestbook -c "SELECT COUNT(*) as total_visitors FROM visitors;"
