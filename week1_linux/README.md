# Week 1: Linux Fundamentals

## Environment
- **Platform:** AWS EC2 (t2.micro, Amazon Linux 2023)
- **Region:** us-east-2
- **Access:** SSH with key-based authentication

## Scripts Built

### 1. system_monitor.sh
Monitors system health metrics and logs to file.

**What it does:**
- Checks disk usage across all partitions
- Reports memory usage (free/used)
- Shows top 5 CPU-consuming processes
- Tests internet connectivity
- Logs everything with timestamp

**How to run:**
```bash
chmod +x system_monitor.sh
./system_monitor.sh
cat /tmp/system_monitor.log
```

**Example output:**
```
=== System Monitor Report ===
Timestamp: Mon Oct 21 05:45:23 UTC 2025

Disk Usage:
/dev/xvda1      8.0G  1.2G  6.8G  15% /

Memory Usage:
              total        used        free      shared  buff/cache   available
Mem:           964Mi       156Mi       542Mi       0.0Ki       265Mi       667Mi
...
```

### 2. network_check.sh
Tests connectivity to multiple hosts.

**What it does:**
- Pings Google DNS (8.8.8.8)
- Pings Cloudflare DNS (1.1.1.1)
- Pings google.com
- Reports which hosts are reachable

### 3. disk_alert.sh
Alerts if disk usage exceeds threshold.

**What it does:**
- Checks root partition usage
- Compares against 80% threshold
- Alerts if exceeded

## Key Learnings

### Technical Skills
- Bash scripting basics (variables, conditionals, loops)
- Linux system commands (df, free, ps, ping)
- File I/O and logging with redirects (>, >>)
- Process management and monitoring
- SSH key-based authentication
- Git workflow (init, add, commit, push)

### DevOps Concepts
- Working on cloud infrastructure (AWS EC2)
- Infrastructure as code thinking
- Documentation and version control
- Monitoring and observability basics

## What's Next
- Week 2: Docker fundamentals
- Containerize these scripts
- Learn container orchestration basics
