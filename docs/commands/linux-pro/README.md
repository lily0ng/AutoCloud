# Linux Commands: Basic to Professional

<div align="center">

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Bash-%234EAA25.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

**Complete Linux Command Reference: 1000+ Commands**

[![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)](.)
[![Commands](https://img.shields.io/badge/Commands-1000+-blue.svg)](.)
[![Level](https://img.shields.io/badge/Level-Basic%20to%20Pro-orange.svg)](.)

</div>

---

## 📚 Documentation Structure

This comprehensive guide contains **1000+ Linux commands** organized from basic to professional level for all major distributions (Ubuntu, CentOS, RHEL, Debian, Arch).

### 📁 Command Categories

| Category | File | Commands | Level |
|----------|------|----------|-------|
| **File System & Navigation** | [01-filesystem.md](01-filesystem.md) | 180+ | Basic → Advanced |
| **Text Processing & Editing** | [02-text-processing.md](02-text-processing.md) | 150+ | Basic → Pro |
| **System Administration** | [03-system-admin.md](03-system-admin.md) | 200+ | Intermediate → Expert |
| **Network & Connectivity** | [04-network.md](04-network.md) | 140+ | Basic → Pro |
| **Package Management** | [05-package-management.md](05-package-management.md) | 80+ | Intermediate → Advanced |
| **Process & Job Control** | [06-process-management.md](06-process-management.md) | 100+ | Intermediate → Pro |
| **Security & Permissions** | [07-security.md](07-security.md) | 90+ | Advanced → Expert |
| **Shell Scripting & Automation** | [08-scripting.md](08-scripting.md) | 60+ | Advanced → Expert |

---

## 🎯 Quick Start Guide

### Basic Commands (Getting Started)
```bash
ls                  # List files
cd <directory>      # Change directory
pwd                 # Print working directory
mkdir <name>        # Create directory
rm <file>          # Remove file
cp <src> <dest>    # Copy files
mv <src> <dest>    # Move/rename files
```

### Intermediate Commands
```bash
find / -name "*.log"               # Find files
grep -r "pattern" /path            # Search in files
ps aux | grep process              # Find processes
df -h                              # Disk space
du -sh *                           # Directory sizes
top                                # System monitor
```

### Advanced Commands
```bash
awk '{print $1,$3}' file.txt      # Text processing
sed 's/old/new/g' file.txt        # Stream editor
xargs -P 4 command                # Parallel execution
ssh-keygen -t ed25519             # SSH key generation
iptables -A INPUT -p tcp --dport 80 -j ACCEPT  # Firewall
```

---

## 📖 How to Use This Guide

### 🎓 Skill Levels

- 🟢 **Basic**: Essential daily commands
- 🟡 **Intermediate**: System administration basics
- 🟠 **Advanced**: Complex operations and scripting
- 🔴 **Professional**: Enterprise-level administration
- ⚫ **Expert**: Advanced system optimization

### 💡 Command Format

Each command includes:
- **Syntax**: Command structure with options
- **Description**: Purpose and functionality
- **Examples**: Practical use cases
- **Options**: Available flags and parameters
- **Notes**: Tips, warnings, and best practices

### 📌 Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Safe command |
| ⚠️ | Use with caution |
| 🔒 | Requires root/sudo |
| 🐧 | All distributions |
| 📦 | Debian/Ubuntu specific |
| 🎩 | RHEL/CentOS specific |
| 🌐 | Network related |

---

## 🚀 Essential Commands by Task

### File & Directory Operations
- [Basic File Operations](01-filesystem.md#basic-operations)
- [Advanced File Management](01-filesystem.md#advanced-operations)
- [File Permissions](07-security.md#permissions)

### System Administration
- [User Management](03-system-admin.md#user-management)
- [Service Control](03-system-admin.md#service-management)
- [System Monitoring](03-system-admin.md#monitoring)

### Network Operations
- [Network Configuration](04-network.md#configuration)
- [Network Diagnostics](04-network.md#diagnostics)
- [Remote Access](04-network.md#remote-access)

### Package Management
- [APT (Debian/Ubuntu)](05-package-management.md#apt)
- [YUM/DNF (RHEL/CentOS)](05-package-management.md#yum-dnf)
- [Pacman (Arch)](05-package-management.md#pacman)

---

## 🎯 Command Categories Overview

### 1️⃣ File System & Navigation (180+ commands)

<details>
<summary>Click to expand</summary>

#### Basic Operations
- ls, cd, pwd, mkdir, rmdir, rm, cp, mv, touch
- cat, more, less, head, tail, file, stat

#### Advanced Operations
- find, locate, which, whereis, tree
- ln, symlink, readlink, realpath
- chown, chmod, chgrp, umask

#### Disk & Storage
- df, du, fdisk, parted, mkfs, mount, umount
- lsblk, blkid, dd, sync, fsck

</details>

### 2️⃣ Text Processing & Editing (150+ commands)

<details>
<summary>Click to expand</summary>

#### Text Viewing & Manipulation
- cat, tac, more, less, head, tail, nl
- cut, paste, join, split, fmt, fold

#### Searching & Pattern Matching
- grep, egrep, fgrep, zgrep, ag, ack
- sed, awk, perl, python for text processing

#### Text Editors
- vim, nano, emacs, vi, ed
- gedit, kate, atom, vscode (terminal)

</details>

### 3️⃣ System Administration (200+ commands)

<details>
<summary>Click to expand</summary>

#### User & Group Management
- useradd, usermod, userdel, groupadd, groupmod
- passwd, chage, id, whoami, who, w, last

#### Service Management
- systemctl, service, init.d scripts
- journalctl, systemd-analyze

#### System Information
- uname, hostname, hostnamectl, uptime
- lsb_release, dmidecode, lshw, lscpu

</details>

### 4️⃣ Network & Connectivity (140+ commands)

<details>
<summary>Click to expand</summary>

#### Network Configuration
- ifconfig, ip, route, arp, hostname
- nmcli, nmtui, netplan, systemd-networkd

#### Network Diagnostics
- ping, traceroute, mtr, nslookup, dig, host
- netstat, ss, lsof, tcpdump, wireshark

#### Remote Access
- ssh, scp, sftp, rsync
- telnet, nc (netcat), socat

</details>

### 5️⃣ Package Management (80+ commands)

<details>
<summary>Click to expand</summary>

#### APT (Debian/Ubuntu)
- apt, apt-get, apt-cache, aptitude
- dpkg, dpkg-query, add-apt-repository

#### YUM/DNF (RHEL/CentOS)
- yum, dnf, rpm, yum-config-manager
- rpm-query, createrepo

#### Other Package Managers
- pacman (Arch), zypper (SUSE)
- snap, flatpak, AppImage

</details>

### 6️⃣ Process & Job Control (100+ commands)

<details>
<summary>Click to expand</summary>

#### Process Management
- ps, top, htop, atop, glances
- kill, killall, pkill, pgrep

#### Job Control
- jobs, fg, bg, nohup, disown
- screen, tmux, byobu

#### Resource Monitoring
- vmstat, iostat, mpstat, sar
- free, uptime, dstat

</details>

### 7️⃣ Security & Permissions (90+ commands)

<details>
<summary>Click to expand</summary>

#### Access Control
- chmod, chown, chgrp, umask, setfacl, getfacl
- sudo, su, visudo

#### Firewall & Security
- iptables, ip6tables, ufw, firewalld
- fail2ban, selinux, apparmor

#### Encryption & Keys
- gpg, openssl, ssh-keygen
- cryptsetup, luks

</details>

### 8️⃣ Shell Scripting & Automation (60+ commands)

<details>
<summary>Click to expand</summary>

#### Shell Features
- Variables, Functions, Loops, Conditions
- Arrays, String Manipulation
- Command Substitution, Pipes, Redirects

#### Automation Tools
- cron, crontab, at, batch
- systemd timers, ansible

#### Script Utilities
- test, expr, bc, dc
- xargs, parallel

</details>

---

## 📊 Command Statistics

| Level | Commands | Percentage |
|-------|----------|------------|
| 🟢 Basic | 200 | 20% |
| 🟡 Intermediate | 250 | 25% |
| 🟠 Advanced | 300 | 30% |
| 🔴 Professional | 170 | 17% |
| ⚫ Expert | 80 | 8% |
| **Total** | **1000+** | **100%** |

---

## 🔍 Command Quick Reference

### Most Used Commands (Top 50)

```bash
# Navigation & Files
ls, cd, pwd, mkdir, rm, cp, mv, touch, cat, less

# Text Processing
grep, sed, awk, cut, sort, uniq, wc, diff

# System Info
top, ps, df, du, free, uname, hostname

# Network
ping, ssh, scp, wget, curl, netstat, ifconfig

# Package Management
apt, yum, dnf, rpm, dpkg

# Permissions
chmod, chown, sudo, su

# Process Control
kill, bg, fg, jobs, screen, tmux

# Compression
tar, gzip, bzip2, zip, unzip

# Search
find, locate, which, whereis
```

---

## 💼 Professional Use Cases

### 1. System Administration
- User and permission management
- Service configuration and monitoring
- System updates and maintenance
- Log analysis and troubleshooting

### 2. DevOps & Automation
- Infrastructure as Code
- Configuration management
- Container orchestration
- CI/CD pipeline automation

### 3. Network Administration
- Network configuration and routing
- Firewall and security rules
- VPN and tunnel configuration
- Traffic monitoring and analysis

### 4. Security Operations
- Security hardening and compliance
- Intrusion detection and prevention
- Access control and auditing
- Vulnerability scanning

---

## 📚 Distribution-Specific Commands

### Ubuntu/Debian
```bash
apt update && apt upgrade           # Update system
apt install package                 # Install package
apt remove package                  # Remove package
dpkg -i package.deb                # Install .deb
systemctl status service           # Check service
```

### RHEL/CentOS
```bash
yum update                         # Update system
yum install package                # Install package
yum remove package                 # Remove package
rpm -ivh package.rpm              # Install .rpm
systemctl status service          # Check service
```

### Arch Linux
```bash
pacman -Syu                       # Update system
pacman -S package                 # Install package
pacman -R package                 # Remove package
pacman -Ss search                 # Search package
systemctl status service          # Check service
```

---

## 🛠️ Essential Shell Scripts

### System Information Script
```bash
#!/bin/bash
echo "=== System Information ==="
echo "Hostname: $(hostname)"
echo "OS: $(lsb_release -d | cut -f2)"
echo "Kernel: $(uname -r)"
echo "Uptime: $(uptime -p)"
echo "CPU: $(nproc) cores"
echo "Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
```

### Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/backup"
SOURCE_DIR="/home/user/data"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf "${BACKUP_DIR}/backup_${DATE}.tar.gz" "${SOURCE_DIR}"
find "${BACKUP_DIR}" -name "backup_*.tar.gz" -mtime +7 -delete
```

### Log Monitoring Script
```bash
#!/bin/bash
LOGFILE="/var/log/syslog"
PATTERN="error|critical|fail"

tail -f "$LOGFILE" | grep --line-buffered -iE "$PATTERN" | \
while read line; do
    echo "[ALERT] $(date '+%Y-%m-%d %H:%M:%S') - $line"
done
```

---

## 🎓 Learning Path

### Beginner (Week 1-2)
1. File system navigation
2. Basic file operations
3. Text viewing and editing
4. Permission basics

### Intermediate (Week 3-4)
5. Process management
6. Package management
7. Network basics
8. Shell scripting fundamentals

### Advanced (Week 5-8)
9. System administration
10. Advanced networking
11. Security and hardening
12. Automation and scripting

### Professional (Week 9-12)
13. Performance tuning
14. High availability setups
15. Disaster recovery
16. Enterprise integration

---

## 📚 Additional Resources

### Official Documentation
- [Linux man pages](https://linux.die.net/man/)
- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)

### Learning Resources
- [The Linux Command Line](http://linuxcommand.org/tlcl.php)
- [Linux Journey](https://linuxjourney.com/)
- [OverTheWire Wargames](https://overthewire.org/wargames/)

### Community
- [r/linux](https://reddit.com/r/linux)
- [Stack Exchange - Unix & Linux](https://unix.stackexchange.com/)
- [Linux Questions](https://www.linuxquestions.org/)

---

## ⚠️ Important Notes

### Safety Guidelines
- ⚠️ Always test commands in a safe environment first
- 🔒 Be careful with commands requiring sudo/root
- 💾 Backup important data before system changes
- 📝 Document configuration changes
- 🔄 Use `--dry-run` or `-n` flags when available

### Best Practices
- Use tab completion for efficiency
- Read man pages before using new commands
- Understand the impact of each command
- Use version control for scripts
- Follow the principle of least privilege

---

## 🆘 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   sudo <command>                    # Run with elevated privileges
   chmod +x script.sh                # Make script executable
   ```

2. **Command Not Found**
   ```bash
   which <command>                   # Check if command exists
   apt install <package>             # Install missing package
   export PATH=$PATH:/new/path       # Add to PATH
   ```

3. **Disk Space Issues**
   ```bash
   df -h                            # Check disk space
   du -sh /* | sort -h              # Find large directories
   journalctl --vacuum-size=100M    # Clean systemd logs
   ```

4. **Network Problems**
   ```bash
   ping 8.8.8.8                     # Test connectivity
   sudo systemctl restart NetworkManager  # Restart network
   ip addr show                     # Check IP configuration
   ```

---

## 🔧 Useful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -alh'
alias la='ls -A'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Shortcuts
alias update='sudo apt update && sudo apt upgrade'
alias ports='netstat -tulanp'
alias myip='curl ifconfig.me'

# System
alias meminfo='free -m -l -t'
alias cpuinfo='lscpu'
alias diskinfo='df -h'

# Logs
alias logs='sudo journalctl -f'
alias syslog='tail -f /var/log/syslog'
```

---

<div align="center">

## 🎓 Ready to Master Linux Commands?

**Start with:** [File System & Navigation →](01-filesystem.md)

---

**Made with ❤️ by 0xff for AutoCloud**

[Back to Main Documentation](../../README.md)

</div>
