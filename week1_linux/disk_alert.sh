#!/bin/bash
# Alert if disk usage exceeds threshold

THRESHOLD=80

usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $usage -gt $THRESHOLD ]; then
  echo "WARNING: Disk usage is ${usage}% (above ${THRESHOLD}% threshold)"
else
  echo "OK: Disk usage is ${usage}% (below ${THRESHOLD}% threshold)"
fi
