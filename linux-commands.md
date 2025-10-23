Complete Linux Commands for Cloud & DevOps
Part 1: File System & Navigation
Basic Navigation
bash# Current location
pwd                           # Print Working Directory - shows where you are

# Change directory
cd /path/to/directory        # Go to specific path (absolute)
cd directory                 # Go to directory (relative to current location)
cd ~                         # Go to home directory (/home/username)
cd                           # Also goes to home (shortcut)
cd ..                        # Go up one level (parent directory)
cd ../..                     # Go up two levels
cd -                         # Go to previous directory (like back button)

# List files and directories
ls                           # List files in current directory
ls -l                        # Long format (detailed: permissions, owner, size, date)
ls -a                        # Show hidden files (files starting with .)
ls -la                       # Long format + hidden files (most complete view)
ls -lh                       # Long format with human-readable sizes (KB, MB, GB)
ls -lt                       # Sort by modification time (newest first)
ls -ltr                      # Sort by time, reverse order (oldest first)
ls -lS                       # Sort by size (largest first)
ls -R                        # Recursive (show subdirectories)
ls /path/to/dir              # List specific directory
ls *.txt                     # List only .txt files (wildcard)

# Tree view (visual hierarchy)
tree                         # Show directory tree (install: sudo yum install tree)
tree -L 2                    # Limit to 2 levels deep
tree -d                      # Only directories
Real DevOps use cases:
bash# Find large log files
ls -lhS /var/log | head -10

# Find recently modified configs
ls -lt /etc | head -5

# Check hidden config files in home
ls -la ~ | grep "^\."

File & Directory Operations
bash# Create
mkdir directory_name         # Make directory
mkdir -p path/to/nested/dir  # Create nested directories (parents too)
touch file.txt               # Create empty file or update timestamp
touch file{1..10}.txt        # Create file1.txt through file10.txt

# Copy
cp source.txt destination.txt           # Copy file
cp source.txt /path/to/destination/     # Copy to directory
cp -r directory/ /destination/          # Copy directory (recursive)
cp -i source.txt dest.txt               # Interactive (ask before overwrite)
cp -p source.txt dest.txt               # Preserve permissions and timestamps
cp -v source.txt dest.txt               # Verbose (show what's being copied)

# Move/Rename
mv old_name.txt new_name.txt            # Rename file
mv file.txt /path/to/destination/       # Move file
mv -i source.txt dest.txt               # Interactive (ask before overwrite)
mv directory/ /new/location/            # Move directory

# Remove/Delete
rm file.txt                             # Remove file
rm -i file.txt                          # Interactive (ask confirmation)
rm -f file.txt                          # Force (no questions asked)
rm -r directory/                        # Remove directory recursively
rm -rf directory/                       # Force remove directory (DANGEROUS!)
rmdir empty_directory                   # Remove empty directory only

# IMPORTANT: There's NO trash/recycle bin - deleted = gone forever!
DevOps safety patterns:
bash# Always test with echo first
echo rm -rf /path/*          # See what would be deleted

# Use -i for important operations
alias rm='rm -i'             # Make rm always ask
alias cp='cp -i'             # Make cp always ask
alias mv='mv -i'             # Make mv always ask

# Backup before removing
cp -r /etc/nginx /backup/ && rm -rf /etc/nginx

Viewing File Contents
bash# View entire file
cat file.txt                            # Print all contents
cat file1.txt file2.txt                 # Concatenate multiple files
cat -n file.txt                         # Show line numbers

# View with pagination
less file.txt                           # Page through file (space: next page, b: back, q: quit)
more file.txt                           # Similar to less (older)

# View beginning
head file.txt                           # First 10 lines
head -n 20 file.txt                     # First 20 lines
head -c 100 file.txt                    # First 100 bytes

# View end
tail file.txt                           # Last 10 lines
tail -n 50 file.txt                     # Last 50 lines
tail -f file.txt                        # Follow file (CRITICAL for live logs)
tail -F file.txt                        # Follow even if file rotates

# View specific lines
sed -n '10,20p' file.txt                # Lines 10-20
awk 'NR==5' file.txt                    # Line 5 only

# Count lines/words/characters
wc file.txt                             # Lines, words, characters
wc -l file.txt                          # Lines only
wc -w file.txt                          # Words only
wc -c file.txt                          # Characters only
Real-world examples:
bash# Monitor live application logs
tail -f /var/log/app.log

# Check last 100 errors
tail -n 100 /var/log/error.log

# See first few lines of config
head -n 20 /etc/nginx/nginx.conf

# Count number of users
wc -l /etc/passwd

# Watch logs for errors
tail -f /var/log/syslog | grep -i error
```

---

## Part 2: File Permissions & Ownership

### Understanding Permissions

**Symbolic notation:**
```
-rwxr-xr--
│││││││││
│││││││└└─ Others: read only (r--)
││││││└└└─ Group: read + execute (r-x)
│││└└└└└└─ Owner: read + write + execute (rwx)
└───────── File type: - (regular file)

d = directory
l = symbolic link
b = block device
c = character device
```

**Numeric notation:**
```
r (read)    = 4
w (write)   = 2  
x (execute) = 1

rwx = 4+2+1 = 7
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
Changing Permissions
bash# Numeric method (most common in DevOps)
chmod 755 script.sh          # rwxr-xr-x (owner: all, others: read+execute)
chmod 644 file.txt           # rw-r--r-- (owner: read+write, others: read)
chmod 600 secret.key         # rw------- (owner only, most secure)
chmod 700 private_script.sh  # rwx------ (owner only can execute)
chmod 777 file.txt           # rwxrwxrwx (everyone - AVOID!)

# Symbolic method
chmod u+x script.sh          # Add execute for user (owner)
chmod g+w file.txt           # Add write for group
chmod o-r file.txt           # Remove read for others
chmod a+r file.txt           # Add read for all
chmod u=rwx,g=rx,o=r file    # Set exact permissions

# Recursive (for directories)
chmod -R 755 /var/www        # Apply to all files/dirs inside
chmod -R 644 *.txt           # All txt files

# Special permissions
chmod +t directory           # Sticky bit (only owner can delete)
chmod u+s executable         # SUID (run as owner)
chmod g+s directory          # SGID (inherit group)
Common DevOps permission patterns:
bash# Web server files
chmod 644 index.html         # Files readable by web server
chmod 755 /var/www           # Directories executable

# Application scripts
chmod 755 start.sh           # Scripts executable by owner
chmod 700 deploy.sh          # Sensitive scripts owner-only

# Configuration files
chmod 644 app.conf           # Readable by services
chmod 600 database.conf      # Sensitive configs owner-only

# SSH keys
chmod 600 ~/.ssh/id_rsa      # Private key (must be 600)
chmod 644 ~/.ssh/id_rsa.pub  # Public key
chmod 700 ~/.ssh             # SSH directory

# Docker socket
chmod 666 /var/run/docker.sock  # Allow non-root Docker access
Changing Ownership
bash# Change owner
chown user file.txt          # Change owner
chown user:group file.txt    # Change owner and group
chown :group file.txt        # Change group only
chown -R user:group /dir     # Recursive

# Change group only
chgrp group file.txt         # Change group
chgrp -R group /dir          # Recursive

# Real examples
sudo chown ec2-user:ec2-user /var/www
sudo chown nginx:nginx /var/log/nginx
sudo chown -R 1000:1000 /app  # Numeric UID:GID

Part 3: Searching & Finding
Find Files
bash# Find by name
find /path -name "filename"              # Exact name
find /path -name "*.txt"                 # Pattern (wildcard)
find /path -iname "*.TXT"                # Case insensitive

# Find by type
find /path -type f                       # Files only
find /path -type d                       # Directories only
find /path -type l                       # Symbolic links

# Find by size
find /path -size +100M                   # Larger than 100MB
find /path -size -1M                     # Smaller than 1MB
find /path -size 50M                     # Exactly 50MB

# Find by time
find /path -mtime -7                     # Modified in last 7 days
find /path -mtime +30                    # Modified more than 30 days ago
find /path -atime -1                     # Accessed in last day
find /path -ctime -7                     # Changed in last 7 days

# Find by permissions
find /path -perm 777                     # Exactly 777
find /path -perm -644                    # At least 644
find /path -perm /u+x                    # User executable

# Find and execute
find /path -name "*.log" -delete         # Find and delete
find /path -name "*.txt" -exec cat {} \; # Find and cat each
find /path -type f -exec chmod 644 {} \; # Find and chmod

# Combined conditions
find /var/log -name "*.log" -mtime +30 -size +100M
Real DevOps use cases:
bash# Find large log files
find /var/log -name "*.log" -size +100M

# Find files modified today
find /etc -type f -mtime 0

# Find world-writable files (security risk)
find /home -perm -002

# Find and compress old logs
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;

# Find empty files
find /tmp -type f -empty

# Find files owned by specific user
find /home -user ec2-user

# Clean up old temp files
find /tmp -type f -mtime +7 -delete
Search Inside Files
bash# Basic grep
grep "pattern" file.txt                  # Find pattern in file
grep "error" *.log                       # Search in all .log files
grep -r "error" /var/log                 # Recursive search in directory

# grep options
grep -i "error" file.txt                 # Case insensitive
grep -v "info" file.txt                  # Invert match (exclude)
grep -n "error" file.txt                 # Show line numbers
grep -c "error" file.txt                 # Count matches
grep -l "error" *.log                    # Show filenames only
grep -w "error" file.txt                 # Match whole word only

# Context lines
grep -A 5 "error" file.txt               # Show 5 lines After match
grep -B 5 "error" file.txt               # Show 5 lines Before match
grep -C 5 "error" file.txt               # Show 5 lines Context (both sides)

# Multiple patterns
grep -E "error|warning" file.txt         # OR condition (regex)
grep -e "error" -e "warning" file.txt    # Same as above
grep "error" file.txt | grep "database"  # AND condition (pipe)

# Exclude patterns
grep "error" --exclude="*.txt" *         # Exclude .txt files
grep -r "error" --exclude-dir=node_modules /app  # Exclude directory
Production troubleshooting patterns:
bash# Find all errors in last hour
grep "error" /var/log/app.log | grep "$(date +%H):"

# Count errors by type
grep -i error /var/log/app.log | cut -d: -f3 | sort | uniq -c

# Find API errors
grep "API" /var/log/app.log | grep "50[0-9]"

# Exclude INFO logs
grep -v "INFO" /var/log/app.log | grep -E "ERROR|WARN"

# Find errors with context
grep -C 3 "500 Internal Server Error" /var/log/nginx/access.log

# Search across multiple logs
grep -r "connection refused" /var/log/

# Find slow queries
grep "slow query" /var/log/mysql/slow.log | wc -l
Locate (Fast Find)
bash# Update locate database (run first)
sudo updatedb

# Find files by name (very fast)
locate filename
locate -i filename                       # Case insensitive
locate -c filename                       # Count only
locate -r "regex_pattern"                # Regex search

# Limit results
locate -n 10 filename                    # First 10 results

Part 4: Text Processing (DevOps Essential)
sed (Stream Editor)
bash# Basic replacement
sed 's/old/new/' file.txt                # Replace first occurrence per line
sed 's/old/new/g' file.txt               # Replace all occurrences (global)
sed 's/old/new/2' file.txt               # Replace second occurrence only

# Edit file in-place
sed -i 's/old/new/g' file.txt            # Modify file directly
sed -i.bak 's/old/new/g' file.txt        # Create backup first

# Delete lines
sed '5d' file.txt                        # Delete line 5
sed '5,10d' file.txt                     # Delete lines 5-10
sed '/pattern/d' file.txt                # Delete lines matching pattern

# Print specific lines
sed -n '10p' file.txt                    # Print line 10
sed -n '10,20p' file.txt                 # Print lines 10-20
sed -n '/pattern/p' file.txt             # Print lines matching pattern

# Multiple operations
sed -e 's/old/new/' -e 's/foo/bar/' file.txt
Real examples:
bash# Change port in config
sed -i 's/port: 8080/port: 9090/' config.yaml

# Remove comment lines
sed '/^#/d' file.txt

# Add line number
sed = file.txt | sed 'N;s/\n/\t/'

# Replace in multiple files
sed -i 's/localhost/0.0.0.0/g' *.conf
awk (Pattern Scanning)
bash# Print columns
awk '{print $1}' file.txt                # First column
awk '{print $1,$3}' file.txt             # Columns 1 and 3
awk '{print $NF}' file.txt               # Last column
awk '{print $1,$NF}' file.txt            # First and last

# Field separator
awk -F: '{print $1}' /etc/passwd         # Use : as separator
awk -F, '{print $2}' data.csv            # Use , as separator

# Conditions
awk '$3 > 100' file.txt                  # Lines where column 3 > 100
awk '$1 == "error"' file.txt             # Lines where column 1 = "error"
awk 'NR > 10' file.txt                   # Lines after line 10

# Calculations
awk '{sum+=$1} END {print sum}' file.txt # Sum of first column
awk '{print $1*2}' file.txt              # Double first column

# Pattern matching
awk '/error/ {print $0}' file.txt        # Lines containing "error"
awk '/error/ {print $2}' file.txt        # Column 2 of lines with "error"
DevOps awk magic:
bash# Get memory usage
free -h | awk 'NR==2 {print $3}'

# Process CPU usage
ps aux | awk '{print $1, $3}' | sort -k2 -nr | head -10

# Nginx access log analysis
awk '{print $1}' access.log | sort | uniq -c | sort -nr  # Count IPs

# Calculate average response time
awk '{sum+=$NF} END {print sum/NR}' response_times.log

# Extract specific fields from CSV
awk -F, '{print $2,$5}' data.csv

# Print lines between patterns
awk '/START/,/END/' file.txt
cut (Extract Columns)
bash# By delimiter
cut -d: -f1 /etc/passwd                  # First field (delimiter :)
cut -d: -f1,3 /etc/passwd                # Fields 1 and 3
cut -d, -f2-5 data.csv                   # Fields 2 through 5

# By character position
cut -c1-5 file.txt                       # Characters 1-5
cut -c1,5,10 file.txt                    # Characters 1, 5, and 10
sort & uniq
bash# Sort
sort file.txt                            # Alphabetical
sort -n file.txt                         # Numeric
sort -r file.txt                         # Reverse
sort -u file.txt                         # Unique (remove duplicates)
sort -k2 file.txt                        # Sort by 2nd column
sort -t: -k3 -n /etc/passwd              # Numeric sort on 3rd field

# Unique values
uniq file.txt                            # Remove adjacent duplicates
uniq -c file.txt                         # Count occurrences
uniq -d file.txt                         # Show duplicates only
uniq -u file.txt                         # Show unique only

# Sort and uniq together (most common)
sort file.txt | uniq                     # Remove all duplicates
sort file.txt | uniq -c                  # Count unique lines
sort file.txt | uniq -c | sort -nr       # Most frequent first
Real use cases:
bash# Top 10 IP addresses in access log
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -10

# Count HTTP status codes
cat access.log | awk '{print $9}' | sort | uniq -c

# Find duplicate files
find . -type f -exec md5sum {} \; | sort | uniq -d -w32

# Sort log files by timestamp
sort -t' ' -k4 access.log

Part 5: Process Management
Viewing Processes
bash# Basic process listing
ps                                       # Current terminal processes
ps aux                                   # All processes (BSD style)
ps -ef                                   # All processes (Unix style)
ps -u username                           # User's processes
ps -C nginx                              # Processes by name

# Process tree
pstree                                   # Visual hierarchy
pstree -p                                # Include PIDs
pstree username                          # User's process tree

# Real-time monitoring
top                                      # Interactive process viewer
htop                                     # Better top (install: sudo yum install htop)

# Top keyboard shortcuts:
# k = kill process
# r = renice (change priority)
# M = sort by memory
# P = sort by CPU
# q = quit

# Filter by process name
ps aux | grep nginx
ps aux | grep -v grep | grep nginx       # Exclude grep itself

# Show threads
ps -eLf                                  # All threads
```

**Understanding ps aux output:**
```
USER   PID %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
root     1  0.0  0.1  19232  1234 ?     Ss   10:00   0:01 /sbin/init
│        │   │    │      │     │   │     │      │      │    └─ Command
│        │   │    │      │     │   │     │      │      └─ CPU time
│        │   │    │      │     │   │     │      └─ Start time
│        │   │    │      │     │   │     └─ Process state
│        │   │    │      │     │   └─ Terminal
│        │   │    │      │     └─ Resident memory (actual RAM used)
│        │   │    │      └─ Virtual memory size
│        │   │    └─ Memory percentage
│        │   └─ CPU percentage
│        └─ Process ID
└─ Owner
Process states (STAT):

R = Running
S = Sleeping (waiting)
D = Uninterruptible sleep (I/O)
Z = Zombie (dead but not reaped)
T = Stopped
< = High priority
N = Low priority
s = Session leader

Managing Processes
bash# Background processes
command &                                # Run in background
nohup command &                          # Keep running after logout
nohup command > output.log 2>&1 &       # Redirect all output

# Job control
jobs                                     # List background jobs
fg                                       # Bring to foreground
fg %1                                    # Bring job 1 to foreground
bg                                       # Resume in background
Ctrl+Z                                   # Suspend current process

# Process priority
nice -n 10 command                       # Start with priority 10
renice -n 5 -p PID                       # Change priority of running process
# Priority: -20 (highest) to 19 (lowest), default 0

# Kill processes
kill PID                                 # Graceful termination (SIGTERM)
kill -9 PID                              # Force kill (SIGKILL)
kill -15 PID                             # Same as kill PID
kill -1 PID                              # Reload config (SIGHUP)
killall process_name                     # Kill by name
pkill pattern                            # Kill by pattern
pkill -u username                        # Kill user's processes

# Kill multiple
kill $(ps aux | grep 'python app.py' | awk '{print $2}')
pkill -f "python app.py"                 # Easier way
Common signals:
bashkill -l                                  # List all signals

# Most used:
-1  SIGHUP    Reload config
-2  SIGINT    Interrupt (Ctrl+C)
-9  SIGKILL   Force kill (cannot be caught)
-15 SIGTERM   Graceful termination (default)
-18 SIGCONT   Continue if stopped
-19 SIGSTOP   Stop process
Real scenarios:
bash# Restart nginx gracefully
sudo kill -HUP $(cat /var/run/nginx.pid)

# Find and kill hung process
ps aux | grep hung_process
kill -9 PID

# Kill all Python processes
pkill -9 python

# Stop Docker containers
docker stop $(docker ps -q)

# Find process using port 8080
sudo lsof -i :8080
kill $(sudo lsof -t -i :8080)

Part 6: System Information
System Details
bash# System information
uname -a                                 # All system info
uname -r                                 # Kernel version
uname -m                                 # Machine architecture
hostname                                 # System hostname
hostname -I                              # IP addresses

# OS information
cat /etc/os-release                      # OS details
lsb_release -a                           # Distribution info (if available)
cat /etc/*-release                       # All release files

# Hardware information
lscpu                                    # CPU architecture
cat /proc/cpuinfo                        # Detailed CPU info
lsmem                                    # Memory info
free -h                                  # Memory usage (human readable)
df -h                                    # Disk usage
lsblk                                    # Block devices (disks)
lspci                                    # PCI devices
lsusb                                    # USB devices

# Uptime & load
uptime                                   # How long system running
uptime -p                                # Pretty format
w                                        # Who's logged in + uptime
who                                      # Who's logged in
last                                     # Login history
Disk Usage
bash# Filesystem usage
df                                       # Disk free space
df -h                                    # Human readable (GB, MB)
df -h /                                  # Specific filesystem
df -i                                    # Inode usage
df -T                                    # Include filesystem type

# Directory usage
du -sh *                                 # Size of each item
du -sh /var/log                          # Total size of directory
du -h --max-depth=1                      # One level deep
du -h --max-depth=1 | sort -hr           # Sorted by size
du -ch *.log                             # Total of .log files

# Find large files
du -a / | sort -n -r | head -n 20        # 20 largest files
find / -type f -size +100M               # Files > 100MB
Disk cleanup examples:
bash# Find largest directories
du -h /var | sort -hr | head -20

# Find old logs to delete
find /var/log -name "*.log" -mtime +30

# Check what's filling up disk
df -h | grep -v tmpfs
sudo du -sh /* | sort -hr | head -10
Memory & CPU
bash# Memory
free                                     # Memory usage (bytes)
free -h                                  # Human readable
free -m                                  # In megabytes
free -g                                  # In gigabytes
free -s 5                                # Update every 5 seconds

# CPU usage
mpstat                                   # CPU statistics
mpstat -P ALL                            # Per-CPU stats
iostat                                   # CPU and I/O stats
vmstat                                   # Virtual memory stats
vmstat 5                                 # Update every 5 seconds

# Load average
uptime                                   # Current load
cat /proc/loadavg                        # Load average file
# 3 numbers: 1-min, 5-min, 15-min averages
# Good: < number of CPUs
# Bad: > number of CPUs

Part 7: Networking
Network Configuration
bash# IP addresses
ip addr                                  # Show IP addresses
ip addr show eth0                        # Specific interface
ip -4 addr                               # IPv4 only
ip -6 addr                               # IPv6 only
ifconfig                                 # Old way (deprecated)

# Routing
ip route                                 # Routing table
ip route show                            # Same as above
route -n                                 # Old way

# DNS
cat /etc/resolv.conf                     # DNS servers
nslookup domain.com                      # DNS lookup
dig domain.com                           # DNS lookup (detailed)
host domain.com                          # Simple DNS lookup
Network Testing
bash# Connectivity
ping google.com                          # Test connectivity
ping -c 4 google.com                     # Send 4 packets only
ping -i 0.2 google.com                   # Faster (0.2s interval)

# Traceroute
traceroute google.com                    # Path to destination
traceroute -n google.com                 # No DNS resolution
tracepath google.com                     # Alternative (no root needed)

# Port testing
telnet host port                         # Test if port open
nc -zv host port                         # Netcat port check
curl -v telnet://host:port               # Curl port check

# Download/Upload speed
curl -o /dev/null http://speedtest.tele2.net/10MB.zip  # Download test
wget -O /dev/null http://speedtest.tele2.net/10MB.zip  # Same with wget
Listening Ports & Connections
bash# Listening ports
netstat -tulpn                           # All listening ports
netstat -tulpn | grep LISTEN             # Just listening
netstat -an | grep LISTEN                # Without service names

# Modern alternative (ss)
ss -tulpn                                # Listening ports
ss -tuln                                 # Without PIDs
ss -t                                    # TCP only
ss -u                                    # UDP only

# Established connections
netstat -an | grep ESTABLISHED
ss | grep ESTABLISHED

# Find what's using port 8080
sudo lsof -i :8080
sudo netstat -tulpn | grep :8080
sudo ss -tulpn | grep :8080

# Count connections by state
netstat -ant | awk '{print $6}' | sort | uniq -c

# Check specific port
sudo lsof -i TCP:80
sudo lsof -i UDP:53
Firewall
bash# Check firewall status
sudo systemctl status firewalld          # Amazon Linux 2023
sudo ufw status                          # Ubuntu

# Firewalld commands
sudo firewall-cmd --list-all             # Show all rules
sudo firewall-cmd --add-port=80/tcp      # Open port (temporary)
sudo firewall-cmd --add-port=80/tcp --permanent  # Permanent
sudo firewall-cmd --reload               # Apply changes
sudo firewall-cmd --remove-port=80/tcp --permanent
Download Files
bash# wget
wget URL                                 # Download file
wget -O newname URL                      # Save with different name
wget -c URL                              # Continue interrupted download
wget -b URL                              # Background download
wget --limit-rate=1m URL                 # Limit speed to 1MB/s

# curl
curl URL                                 # Print to stdout
curl -O URL                              # Save with original name
curl -o newname URL                      # Save with new name
curl -L URL                              # Follow redirects
curl -I URL                              # Headers only
curl -s URL                              # Silent (no progress)
curl -X POST -d "data" URL               # POST request
curl -H "Header: value" URL              # Custom header
Real examples:
bash# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Get public IP
curl ifconfig.me
curl icanhazip.com

# Test API
curl -X GET https://api.example.com/users
curl -X POST -H "Content-Type: application/json" -d '{"name":"John"}' https://api.example.com/users

# Download and extract
wget https://example.com/file.tar.gz && tar xzf file.tar.gz

Part 8: Compression & Archives
tar (Tape Archive)
bash# Create archives
tar -czf archive.tar.gz directory/       # Create gzip compressed
tar -cjf archive.tar.bz2 directory/      # Create bzip2 compressed
tar -cf archive.tar directory/           # Create uncompressed

# Extract archives
tar -xzf archive.tar.gz                  # Extract gzip
tar -xjf archive.tar.bz2                 # Extract bzip2
tar -xf archive.tar                      # Extract uncompressed
tar -xzf archive.tar.gz -C /destination/ # Extract to specific location

# View contents
tar -tzf archive.tar.gz                  # List contents (gzip)
tar -tf archive.tar                      # List contents

# Flags explained:
# c = create
# x = extract
# z = gzip
# j = bzip2
# f = file
# v = verbose
# t = listRetryClaude does not have the ability to run the code it generates yet.HContinue
Part 8: Compression & Archives (Continued)
gzip, bzip2, xz
bash# gzip (fast compression)
gzip file.txt                            # Compress (creates file.txt.gz, removes original)
gzip -k file.txt                         # Keep original
gzip -9 file.txt                         # Maximum compression
gunzip file.txt.gz                       # Decompress
gzip -d file.txt.gz                      # Also decompress

# bzip2 (better compression, slower)
bzip2 file.txt                           # Compress (creates file.txt.bz2)
bzip2 -k file.txt                        # Keep original
bunzip2 file.txt.bz2                     # Decompress

# xz (best compression, slowest)
xz file.txt                              # Compress (creates file.txt.xz)
xz -k file.txt                           # Keep original
unxz file.txt.xz                         # Decompress

# View compressed files without extracting
zcat file.txt.gz                         # View gzipped file
zless file.txt.gz                        # Page through gzipped file
bzcat file.txt.bz2                       # View bzip2 file
xzcat file.txt.xz                        # View xz file
zip/unzip
bash# Create zip
zip archive.zip file.txt                 # Single file
zip -r archive.zip directory/            # Recursive (directory)
zip -r -9 archive.zip directory/         # Maximum compression
zip -e archive.zip file.txt              # Encrypted (password)

# Extract zip
unzip archive.zip                        # Extract all
unzip archive.zip -d /destination/       # Extract to location
unzip -l archive.zip                     # List contents
unzip -t archive.zip                     # Test integrity

# Update zip
zip -u archive.zip newfile.txt           # Add/update file
zip -d archive.zip file.txt              # Delete from archive
Real DevOps examples:
bash# Backup logs
tar -czf logs-$(date +%Y%m%d).tar.gz /var/log

# Backup database
mysqldump database | gzip > backup.sql.gz

# Compress old logs
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;

# Extract and pipe
tar -xzf backup.tar.gz --to-stdout file.txt | grep "error"

# Create timestamped backup
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz /app

# Exclude files
tar -czf archive.tar.gz --exclude='*.log' --exclude='node_modules' /app

# Split large archive
tar -czf - /large/directory | split -b 1G - archive.tar.gz.part
# Reassemble
cat archive.tar.gz.part* | tar -xzf -

Part 9: User & Group Management
User Operations
bash# View users
whoami                                   # Current user
id                                       # User ID and groups
id username                              # Info about specific user
users                                    # Currently logged in users
who                                      # Who is logged in (detailed)
w                                        # Who + what they're doing
last                                     # Login history
lastlog                                  # Last login per user

# User files
cat /etc/passwd                          # User database
cat /etc/shadow                          # Password hashes (root only)
cat /etc/group                           # Group database

# Add user
sudo useradd username                    # Basic user creation
sudo useradd -m username                 # Create with home directory
sudo useradd -m -s /bin/bash username    # Specify shell
sudo useradd -m -G docker,sudo username  # Add to groups

# Set password
sudo passwd username                     # Set user password
passwd                                   # Change your own password

# Modify user
sudo usermod -aG docker username         # Add to group (append)
sudo usermod -s /bin/bash username       # Change shell
sudo usermod -l newname oldname          # Rename user
sudo usermod -L username                 # Lock account
sudo usermod -U username                 # Unlock account

# Delete user
sudo userdel username                    # Delete user (keep home)
sudo userdel -r username                 # Delete user + home directory

# Switch user
su username                              # Switch user (need password)
su - username                            # Switch with environment
sudo su -                                # Become root
sudo -i                                  # Root shell
sudo -u username command                 # Run as specific user
Group Operations
bash# View groups
groups                                   # Your groups
groups username                          # User's groups
cat /etc/group                           # All groups

# Create group
sudo groupadd groupname                  # Create group
sudo groupadd -g 1500 groupname          # With specific GID

# Add user to group
sudo usermod -aG groupname username      # Append to group
sudo gpasswd -a username groupname       # Alternative method

# Remove user from group
sudo gpasswd -d username groupname       # Remove from group
sudo usermod -G group1,group2 username   # Set groups (removes others)

# Delete group
sudo groupdel groupname                  # Delete group

# Change file group
sudo chgrp groupname file.txt            # Change group
sudo chgrp -R groupname /directory       # Recursive
Real scenarios:
bash# Add user to docker group (no sudo needed)
sudo usermod -aG docker $USER
newgrp docker                            # Activate group immediately

# Create deployment user
sudo useradd -m -s /bin/bash -G docker deploy
sudo passwd deploy

# Lock/unlock account
sudo usermod -L username                 # Lock (disable login)
sudo usermod -U username                 # Unlock

# Set password expiry
sudo chage -l username                   # View password policy
sudo chage -M 90 username                # Expire after 90 days
sudo chage -d 0 username                 # Force password change on next login

Part 10: System Services (systemd)
Service Management
bash# Check service status
sudo systemctl status service-name       # Detailed status
sudo systemctl is-active service-name    # Just active/inactive
sudo systemctl is-enabled service-name   # Check if auto-start enabled

# Start/Stop/Restart services
sudo systemctl start service-name        # Start service
sudo systemctl stop service-name         # Stop service
sudo systemctl restart service-name      # Stop then start
sudo systemctl reload service-name       # Reload config (no restart)
sudo systemctl reload-or-restart service-name  # Try reload, restart if needed

# Enable/Disable auto-start
sudo systemctl enable service-name       # Start on boot
sudo systemctl disable service-name      # Don't start on boot
sudo systemctl enable --now service-name # Enable and start immediately

# List services
systemctl list-units --type=service      # All loaded services
systemctl list-units --type=service --state=running  # Running only
systemctl list-unit-files --type=service # All available services

# View service logs
sudo journalctl -u service-name          # All logs for service
sudo journalctl -u service-name -f       # Follow logs (live)
sudo journalctl -u service-name --since today
sudo journalctl -u service-name --since "1 hour ago"
sudo journalctl -u service-name -n 50    # Last 50 lines

# Service dependencies
systemctl list-dependencies service-name # What it depends on
systemctl list-dependencies --reverse service-name  # What depends on it
Common services:
bash# Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker

# Nginx
sudo systemctl start nginx
sudo systemctl reload nginx              # Reload config
sudo systemctl status nginx

# SSH
sudo systemctl status sshd
sudo systemctl restart sshd

# PostgreSQL
sudo systemctl start postgresql
sudo systemctl status postgresql

# Firewall
sudo systemctl status firewalld
sudo systemctl stop firewalld
Journalctl (System Logs)
bash# View logs
sudo journalctl                          # All logs
sudo journalctl -f                       # Follow (tail -f style)
sudo journalctl -r                       # Reverse (newest first)
sudo journalctl -n 100                   # Last 100 lines

# Filter by time
sudo journalctl --since today
sudo journalctl --since "2025-10-22"
sudo journalctl --since "1 hour ago"
sudo journalctl --since "10 minutes ago"
sudo journalctl --until "2025-10-22 12:00"
sudo journalctl --since "2025-10-22 10:00" --until "2025-10-22 12:00"

# Filter by service
sudo journalctl -u nginx                 # Nginx logs
sudo journalctl -u docker                # Docker logs
sudo journalctl -u sshd                  # SSH logs

# Filter by priority
sudo journalctl -p err                   # Errors only
sudo journalctl -p warning               # Warnings and above
sudo journalctl -p debug                 # All levels
# Priority levels: emerg, alert, crit, err, warning, notice, info, debug

# Filter by boot
sudo journalctl -b                       # Current boot
sudo journalctl -b -1                    # Previous boot
sudo journalctl --list-boots             # List all boots

# Disk usage
sudo journalctl --disk-usage             # How much space logs use
sudo journalctl --vacuum-size=100M       # Keep only 100MB of logs
sudo journalctl --vacuum-time=1month     # Delete logs older than 1 month

Part 11: Package Management
yum (Amazon Linux, CentOS, RHEL)
bash# Update package list
sudo yum update                          # Update all packages
sudo yum check-update                    # Check for updates

# Install packages
sudo yum install package-name            # Install package
sudo yum install -y package-name         # Yes to all prompts
sudo yum install package1 package2       # Multiple packages

# Remove packages
sudo yum remove package-name             # Uninstall
sudo yum autoremove                      # Remove orphaned dependencies

# Search packages
yum search keyword                       # Search by keyword
yum list available                       # List all available
yum list installed                       # List installed
yum list available | grep keyword        # Search installed

# Package information
yum info package-name                    # Detailed info
yum provides /path/to/file               # Which package provides file

# Clean cache
sudo yum clean all                       # Clean cache
sudo yum makecache                       # Rebuild cache

# Groups
yum grouplist                            # List package groups
sudo yum groupinstall "Development Tools"  # Install group
apt (Ubuntu, Debian)
bash# Update package list
sudo apt update                          # Update package list
sudo apt upgrade                         # Upgrade all packages
sudo apt update && sudo apt upgrade -y   # Both at once

# Install packages
sudo apt install package-name            # Install
sudo apt install -y package-name         # Yes to all
sudo apt install package1 package2       # Multiple packages

# Remove packages
sudo apt remove package-name             # Uninstall
sudo apt purge package-name              # Remove + config files
sudo apt autoremove                      # Remove orphaned dependencies

# Search packages
apt search keyword                       # Search
apt list --installed                     # List installed
apt list --upgradable                    # List upgradable

# Package information
apt show package-name                    # Detailed info
apt-cache policy package-name            # Version info

# Clean cache
sudo apt clean                           # Clean cache
sudo apt autoclean                       # Clean old packages
Common installations:
bash# Development tools
sudo yum groupinstall "Development Tools"
sudo apt install build-essential

# Docker
sudo yum install docker
sudo apt install docker.io

# Python
sudo yum install python3 python3-pip
sudo apt install python3 python3-pip

# Git
sudo yum install git
sudo apt install git

# Nginx
sudo yum install nginx
sudo apt install nginx

# PostgreSQL
sudo yum install postgresql postgresql-server
sudo apt install postgresql postgresql-contrib

# Monitoring tools
sudo yum install htop iotop nethogs
sudo apt install htop iotop nethogs

Part 12: Cron Jobs (Scheduled Tasks)
Crontab Management
bash# Edit crontab
crontab -e                               # Edit your crontab
sudo crontab -e                          # Edit root's crontab
crontab -u username -e                   # Edit user's crontab

# List crontab
crontab -l                               # View your crontab
sudo crontab -l                          # View root's crontab
crontab -u username -l                   # View user's crontab

# Remove crontab
crontab -r                               # Remove your crontab
```

### Cron Syntax
```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
# │ │ │ │ │
# * * * * * command to execute
Examples:
bash# Every minute
* * * * * /path/to/script.sh

# Every 5 minutes
*/5 * * * * /path/to/script.sh

# Every hour at minute 0
0 * * * * /path/to/script.sh

# Every day at 2:30 AM
30 2 * * * /path/to/script.sh

# Every Monday at 9 AM
0 9 * * 1 /path/to/script.sh

# First day of every month at midnight
0 0 1 * * /path/to/script.sh

# Every weekday at 8 AM
0 8 * * 1-5 /path/to/script.sh

# Every 15 minutes between 9 AM and 5 PM
*/15 9-17 * * * /path/to/script.sh
Real DevOps cron jobs:
bash# Backup database daily at 2 AM
0 2 * * * /usr/local/bin/backup-db.sh >> /var/log/backup.log 2>&1

# Clean old logs every Sunday at 3 AM
0 3 * * 0 find /var/log -name "*.log" -mtime +30 -delete

# Monitor disk space every hour
0 * * * * df -h | mail -s "Disk Space Report" admin@example.com

# Restart application at midnight
0 0 * * * systemctl restart myapp

# Pull latest code every 5 minutes
*/5 * * * * cd /app && git pull origin main

# Cleanup Docker every day at 1 AM
0 1 * * * docker system prune -af >> /var/log/docker-cleanup.log 2>&1

# Health check every minute
* * * * * curl -f http://localhost/health || systemctl restart myapp
Cron Special Strings
bash@reboot    command                       # Run at startup
@yearly    command                       # Run once a year (0 0 1 1 *)
@annually  command                       # Same as @yearly
@monthly   command                       # Run once a month (0 0 1 * *)
@weekly    command                       # Run once a week (0 0 * * 0)
@daily     command                       # Run once a day (0 0 * * *)
@midnight  command                       # Same as @daily
@hourly    command                       # Run once an hour (0 * * * *)

Part 13: Environment Variables
Viewing Variables
bash# View all environment variables
env                                      # List all
printenv                                 # Same as env
printenv PATH                            # Specific variable
echo $PATH                               # Using echo
echo $HOME                               # Home directory
echo $USER                               # Current user
echo $SHELL                              # Current shell
Setting Variables
bash# Temporary (current session only)
export VAR_NAME="value"                  # Export to environment
VAR_NAME="value"                         # Shell variable (not inherited)

# Permanent (for user)
echo 'export VAR_NAME="value"' >> ~/.bashrc
source ~/.bashrc                         # Reload

# Permanent (system-wide)
sudo echo 'export VAR_NAME="value"' >> /etc/environment
sudo echo 'export VAR_NAME="value"' >> /etc/profile

# Unset variable
unset VAR_NAME                           # Remove variable
Important environment variables:
bash# Path
echo $PATH                               # Executable search path
export PATH=$PATH:/new/path              # Add to PATH
export PATH=/new/path:$PATH              # Prepend to PATH

# Common variables
$HOME                                    # User home directory
$USER                                    # Current username
$PWD                                     # Current working directory
$SHELL                                   # Current shell
$TERM                                    # Terminal type
$EDITOR                                  # Default text editor
$LANG                                    # Language/locale
$HOSTNAME                                # System hostname
DevOps environment variables:
bash# Docker
export DOCKER_HOST=tcp://192.168.1.100:2375
export DOCKER_TLS_VERIFY=1

# AWS
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Database
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=mydb
export DB_USER=postgres
export DB_PASSWORD=secret

# Application
export NODE_ENV=production
export PORT=3000
export DEBUG=true

Part 14: SSH & Remote Access
SSH Basics
bash# Connect to remote server
ssh user@hostname                        # Basic connection
ssh user@192.168.1.100                   # Using IP
ssh -p 2222 user@hostname                # Custom port

# SSH with key
ssh -i /path/to/key.pem user@hostname    # Specific key
ssh -i ~/.ssh/id_rsa user@hostname       # Common key location

# SSH options
ssh -v user@hostname                     # Verbose (debug)
ssh -vv user@hostname                    # More verbose
ssh -vvv user@hostname                   # Maximum verbosity
ssh -X user@hostname                     # X11 forwarding
ssh -A user@hostname                     # Agent forwarding
ssh -N -L 8080:localhost:80 user@host    # Port forwarding only
SSH Key Management
bash# Generate key pair
ssh-keygen                               # Interactive generation
ssh-keygen -t rsa -b 4096                # RSA 4096-bit
ssh-keygen -t ed25519                    # Ed25519 (modern, secure)
ssh-keygen -t rsa -b 4096 -C "email@example.com"  # With comment

# Copy public key to server
ssh-copy-id user@hostname                # Copy your key
ssh-copy-id -i ~/.ssh/id_rsa.pub user@host  # Specific key

# Manual key copy
cat ~/.ssh/id_rsa.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Change key permissions (CRITICAL)
chmod 700 ~/.ssh                         # SSH directory
chmod 600 ~/.ssh/id_rsa                  # Private key
chmod 644 ~/.ssh/id_rsa.pub              # Public key
chmod 600 ~/.ssh/authorized_keys         # Authorized keys
chmod 600 ~/.ssh/config                  # SSH config
SSH Config File
Create ~/.ssh/config:
bash# AWS EC2 instance
Host myserver
    HostName 3.133.58.170
    User ec2-user
    IdentityFile ~/.ssh/mykey.pem
    Port 22

# Production server
Host prod
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/deploy_key
    ForwardAgent yes

# All servers with common settings
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
Usage with config:
bashssh myserver                             # Uses config settings
ssh prod                                 # No need to specify user/key
SCP (Secure Copy)
bash# Copy to remote
scp file.txt user@host:/path/to/destination/
scp -r directory/ user@host:/path/to/destination/
scp -P 2222 file.txt user@host:/path/    # Custom port
scp -i key.pem file.txt user@host:/path/ # With key

# Copy from remote
scp user@host:/path/to/file.txt .
scp -r user@host:/path/to/directory/ .

# Copy between remote servers (from local)
scp user1@host1:/file user2@host2:/destination/
RSYNC (Better than SCP)
bash# Basic sync
rsync -avz source/ user@host:/destination/

# Flags explained:
# -a = archive (preserve permissions, times, etc.)
# -v = verbose
# -z = compress during transfer
# -h = human-readable
# -P = show progress + partial transfers

# Common patterns
rsync -avzh source/ user@host:/destination/  # Human readable
rsync -avz --delete source/ dest/            # Delete extra files in dest
rsync -avz --exclude='*.log' source/ dest/   # Exclude pattern
rsync -avz -e "ssh -i key.pem" source/ user@host:/dest/  # With SSH key

# Dry run (test without actually copying)
rsync -avzn source/ dest/                    # -n = dry run

# Resume interrupted transfer
rsync -avzP source/ dest/                    # -P = partial + progress
Real scenarios:
bash# Backup to remote server
rsync -avz --delete /var/www/ backup@server:/backups/www/

# Sync code to production
rsync -avz --exclude='.git' --exclude='node_modules' /app/ user@prod:/app/

# Pull database backups
rsync -avz user@db-server:/backups/ /local/backups/

# Mirror directory
rsync -avz --delete /source/ /destination/

Part 15: Symbolic Links
Creating Links
bash# Symbolic (soft) link
ln -s /path/to/original /path/to/link    # Create symlink
ln -s /usr/share/app /app                # Example

# Hard link
ln /path/to/original /path/to/link       # Create hard link

# Force overwrite
ln -sf /new/target /existing/link        # Update link

# Check if link
ls -l /path/to/link                      # Shows -> target
file /path/to/link                       # Shows "symbolic link"
Difference between symbolic and hard links:
FeatureSymbolic LinkHard LinkPoints toFile pathInode (file data)Crosses filesystemsYesNoLinks to directoriesYesNoOriginal deletedLink breaksLink still worksUsageMost commonRare
Common use cases:
bash# Current version link
ln -sf /app/releases/v2.0 /app/current

# Configuration
ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite

# Python version
ln -sf /usr/bin/python3.9 /usr/bin/python

# Logs
ln -s /var/log/app/app.log /logs/current.log

# Remove symbolic link
rm /path/to/link                         # Remove link (not target)
unlink /path/to/link                     # Alternative

Part 16: Redirection & Pipes
Input/Output Redirection
bash# Output redirection
command > file.txt                       # Redirect stdout to file (overwrite)
command >> file.txt                      # Redirect stdout to file (append)
command 2> error.txt                     # Redirect stderr to file
command > output.txt 2> error.txt        # Redirect both separately
command > output.txt 2>&1                # Redirect both to same file
command &> output.txt                    # Same as above (shorthand)

# Input redirection
command < input.txt                      # Read from file
command << EOF                           # Here document
multi-line
input
EOF

# Discard output
command > /dev/null                      # Discard stdout
command 2> /dev/null                     # Discard stderr
command > /dev/null 2>&1                 # Discard all output
Pipes
bash# Basic pipe
command1 | command2                      # Pass output to input

# Multiple pipes
command1 | command2 | command3

# Tee (output to file AND pipe)
command | tee file.txt                   # View and save
command | tee -a file.txt                # Append to file
command | tee file.txt | command2        # Save and continue pipeline
Powerful pipe combinations:
bash# Count processes
ps aux | wc -l

# Find and sort
ps aux | grep nginx | sort -k3 -nr

# Top 10 largest files
du -ah / 2>/dev/null | sort -hr | head -10

# Count unique IPs
cat access.log | awk '{print $1}' | sort | uniq | wc -l

# Monitor logs
tail -f /var/log/app.log | grep ERROR

# Real-time process monitoring
ps aux | grep python | awk '{print $2,$11}' | column -t

# Network connections by state
netstat -an | awk '{print $6}' | sort | uniq -c | sort -nr

# Disk usage by directory
du -sh /* | sort -hr | head -20

# Failed login attempts
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr

Part 17: Aliases & Functions
Aliases
bash# Create alias
alias ll='ls -la'
alias ..='cd ..'
alias ...='cd ../..'
alias update='sudo yum update -y'
alias dps='docker ps'
alias dstop='docker stop $(docker ps -q)'

# View aliases
alias                                    # List all aliases
alias ll                                 # Show specific alias

# Remove alias
unalias ll                               # Remove alias

# Make permanent
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
Useful DevOps aliases:
bash# Docker
alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias di='docker images'
alias dex='docker exec -it'
alias dlog='docker logs -f'
alias dclean='docker system prune -af'

# Git
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias glog='git log --oneline --graph'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -lah'
alias la='ls -A'

# System
alias ports='netstat -tulanp'
alias meminfo='free -h'
alias diskinfo='df -h'
alias cpuinfo='lscpu'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
Functions
bash# Define function
mkcd() {
    mkdir -p "$1"
    cd "$1"
}

# More complex function
backup() {
    local file="$1"
    local backup_dir="$HOME/backups"
    mkdir -p "$backup_dir"
    cp "$file" "$backup_dir/$(basename $file).$(date +%Y%m%d)"
}

# Docker functions
dsh() {
    docker exec -it "$1" sh
}

dbash() {
    docker exec -it "$1" bash
}

# Git functions
gcom() {
    git add .
    git commit -m "$1"
    git push
}

# Make permanent
echo 'mkcd() { mkdir -p "$1" && cd "$1"; }' >> ~/.bashrc
source ~/.bashrc

Part 18: Quick Reference - Must-Know Commands
Top 50 Commands for DevOps
bash# Navigation & Files (10)
pwd, cd, ls, mkdir, rm, cp, mv, touch, find, cat

# Viewing & Editing (5)
less, head, tail, grep, nano

# Permissions (3)
chmod, chown, chgrp

# Processes (5)
ps, top, kill, systemctl, journalctl

# System Info (5)
df, du, free, uname, uptime

# Networking (7)
ping, curl, wget, netstat, ss, ip, ssh

# Text Processing (5)
awk, sed, cut, sort, uniq

# Compression (3)
tar, gzip, zip

# Package Management (2)
yum/apt install, yum/apt remove

# User Management (3)
useradd, passwd, su

# Others (2)
crontab, ln
Most Common One-Liners
bash# Find large files
find / -type f -size +100M 2>/dev/null

# Count lines in all .py files
find . -name "*.py" | xargs wc -l

# Kill all processes matching pattern
pkill -f "python app.py"

# Monitor disk in real-time
watch -n 1 df -h

# Find files modified in last hour
find . -type f -mmin -60

# Top 10 memory-consuming processes
ps aux --sort=-%mem | head -11

# Check open ports
sudo netstat -tulanp | grep LISTEN

# Backup with timestamp
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz /path

# Remove all stopped Docker containers
docker rm $(docker ps -aq)

# Find and replace in all files
find . -type f -exec sed -i 's/old/new/g' {} +
