#!/bin/bash
# Check connectivity to multiple hosts

HOSTS=("8.8.8.8" "1.1.1.1" "google.com")
LOG_FILE="/tmp/network_check.log"

echo "Network Check - $(date)" > $LOG_FILE

for host in "${HOSTS[@]}"; do
  if ping -c 1 $host &> /dev/null; then
    echo "✓ $host - REACHABLE" >> $LOG_FILE
  else
    echo "✗ $host - UNREACHABLE" >> $LOG_FILE
  fi
done

cat $LOG_FILE
