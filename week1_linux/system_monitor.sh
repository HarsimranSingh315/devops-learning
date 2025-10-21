#!/bin/bash

# Script: System Monitor
# Purpose: Monitor system health and log it

LOG_FILE="/tmp/system_monitor.log"

echo "=== System Monitor Report ===" >> $LOG_FILE
echo "Timestamp: $(date)" >> $LOG_FILE
echo "" >> $LOG_FILE

echo "Disk Usage:" >> $LOG_FILE
df -h | grep -E '^/dev' >> $LOG_FILE
echo "" >> $LOG_FILE

echo "Memory Usage:" >> $LOG_FILE
free -h >> $LOG_FILE
echo "" >> $LOG_FILE

echo "Top 5 CPU Consuming Processes:" >> $LOG_FILE
ps aux --sort=-%cpu | head -6 >> $LOG_FILE
echo "" >> $LOG_FILE

echo "Network Connectivity:" >> $LOG_FILE
ping -c 1 8.8.8.8 >> $LOG_FILE 2>&1 && echo "Internet: UP" >> $LOG_FILE || echo "Internet: DOWN" >> $LOG_FILE
echo "" >> $LOG_FILE

echo "=== End Report ===" >> $LOG_FILE

echo "Monitor report generated at $LOG_FILE"
