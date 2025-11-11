# Windows Commands: Basic to Professional

<div align="center">

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)
![CMD](https://img.shields.io/badge/CMD-4D4D4D?style=for-the-badge&logo=windows-terminal&logoColor=white)

**Complete Windows Command Reference: 1000+ Commands**

[![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)](.)
[![Commands](https://img.shields.io/badge/Commands-1000+-blue.svg)](.)
[![Level](https://img.shields.io/badge/Level-Basic%20to%20Pro-orange.svg)](.)

</div>

---

## 📚 Documentation Structure

This comprehensive guide contains **1000+ Windows commands** organized from basic to professional level.

### 📁 Command Categories

| Category | File | Commands | Level |
|----------|------|----------|-------|
| **System & File Management** | [01-system-file.md](01-system-file.md) | 150+ | Basic → Advanced |
| **Network & Connectivity** | [02-network.md](02-network.md) | 120+ | Basic → Pro |
| **PowerShell Administration** | [03-powershell-admin.md](03-powershell-admin.md) | 200+ | Intermediate → Expert |
| **Active Directory & Domain** | [04-active-directory.md](04-active-directory.md) | 100+ | Advanced → Pro |
| **Security & Permissions** | [05-security.md](05-security.md) | 80+ | Intermediate → Pro |
| **Registry & Configuration** | [06-registry-config.md](06-registry-config.md) | 70+ | Advanced → Expert |
| **Performance & Monitoring** | [07-performance.md](07-performance.md) | 90+ | Intermediate → Pro |
| **Scripting & Automation** | [08-scripting.md](08-scripting.md) | 120+ | Advanced → Expert |
| **Cloud & DevOps Tools** | [09-cloud-devops.md](09-cloud-devops.md) | 70+ | Pro → Expert |

---

## 🎯 Quick Start Guide

### Basic Commands (Getting Started)
```cmd
dir                 # List files
cd <path>          # Change directory  
mkdir <name>       # Create directory
copy <src> <dest>  # Copy files
del <file>         # Delete file
```

### Intermediate Commands
```powershell
Get-ChildItem      # List items
Set-Location       # Change directory
New-Item          # Create item
Copy-Item         # Copy item
Remove-Item       # Remove item
```

### Advanced PowerShell
```powershell
Get-Process | Where-Object {$_.CPU -gt 100}
Get-EventLog -LogName System -Newest 100
Get-Service | Where-Object {$_.Status -eq "Running"}
```

---

## 📖 How to Use This Guide

### 🎓 Skill Levels

- 🟢 **Basic**: Fundamental commands for daily tasks
- 🟡 **Intermediate**: System administration and management
- 🟠 **Advanced**: Complex operations and scripting
- 🔴 **Professional**: Enterprise-level administration
- ⚫ **Expert**: Advanced automation and optimization

### 💡 Command Format

Each command includes:
- **Syntax**: Command structure with parameters
- **Description**: What the command does
- **Examples**: Real-world usage scenarios
- **Options**: Available flags and switches
- **Notes**: Important tips and warnings

### 📌 Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Safe command |
| ⚠️ | Use with caution |
| 🔒 | Requires admin privileges |
| 💻 | PowerShell only |
| 📟 | CMD only |
| 🌐 | Network related |

---

## 🚀 Essential Commands by Task

### File & Directory Management
- [Basic File Operations](01-system-file.md#basic-file-operations)
- [Advanced File Management](01-system-file.md#advanced-file-management)
- [File Permissions](05-security.md#file-permissions)

### System Administration
- [User Management](03-powershell-admin.md#user-management)
- [Service Control](03-powershell-admin.md#service-management)
- [Process Management](07-performance.md#process-management)

### Network Operations
- [Network Configuration](02-network.md#network-configuration)
- [Network Diagnostics](02-network.md#diagnostics)
- [Remote Access](02-network.md#remote-access)

### Security & Permissions
- [User Security](05-security.md#user-security)
- [Firewall Management](05-security.md#firewall)
- [Encryption](05-security.md#encryption)

### Performance & Optimization
- [System Monitoring](07-performance.md#monitoring)
- [Resource Management](07-performance.md#resources)
- [Optimization](07-performance.md#optimization)

---

## 🎯 Command Categories Overview

### 1️⃣ System & File Management (150+ commands)

<details>
<summary>Click to expand</summary>

#### Basic Operations
- dir, cd, mkdir, rmdir, copy, xcopy, move, del, ren, attrib
- type, more, find, findstr, sort, tree, where, which

#### Advanced Operations
- robocopy, icacls, takeown, compact, cipher, fsutil
- diskpart, format, chkdsk, defrag, cleanmgr

#### PowerShell File Operations
- Get-ChildItem, Set-Location, New-Item, Copy-Item, Move-Item
- Remove-Item, Rename-Item, Get-Content, Set-Content, Add-Content
- Select-String, Measure-Object, Compare-Object

</details>

### 2️⃣ Network & Connectivity (120+ commands)

<details>
<summary>Click to expand</summary>

#### Network Configuration
- ipconfig, netsh, route, arp, getmac, hostname
- nslookup, ping, tracert, pathping, netstat

#### Advanced Networking
- Test-Connection, Test-NetConnection, Get-NetAdapter
- Get-NetIPAddress, Get-NetRoute, Get-DnsClientCache
- New-NetFirewallRule, Get-NetFirewallProfile

#### Remote Access
- mstsc, powershell remoting, winrm, psexec
- Enter-PSSession, Invoke-Command, New-PSSession

</details>

### 3️⃣ PowerShell Administration (200+ commands)

<details>
<summary>Click to expand</summary>

#### User & Group Management
- Get-LocalUser, New-LocalUser, Set-LocalUser, Remove-LocalUser
- Get-LocalGroup, Add-LocalGroupMember, Remove-LocalGroupMember

#### Service Management
- Get-Service, Start-Service, Stop-Service, Restart-Service
- Set-Service, New-Service, Remove-Service

#### Process Management
- Get-Process, Start-Process, Stop-Process, Wait-Process
- Debug-Process, Get-WmiObject Win32_Process

</details>

### 4️⃣ Active Directory & Domain (100+ commands)

<details>
<summary>Click to expand</summary>

#### User Management
- Get-ADUser, New-ADUser, Set-ADUser, Remove-ADUser
- Enable-ADAccount, Disable-ADAccount, Unlock-ADAccount

#### Group Management
- Get-ADGroup, New-ADGroup, Add-ADGroupMember
- Remove-ADGroupMember, Get-ADGroupMember

#### Domain Operations
- Get-ADDomain, Get-ADForest, Get-ADDomainController
- Get-ADComputer, Move-ADObject, Get-ADOrganizationalUnit

</details>

### 5️⃣ Security & Permissions (80+ commands)

<details>
<summary>Click to expand</summary>

#### Access Control
- icacls, cacls, Get-Acl, Set-Acl
- takeown, Get-AuthenticodeSignature, Set-AuthenticodeSignature

#### Firewall
- netsh advfirewall, New-NetFirewallRule
- Get-NetFirewallRule, Set-NetFirewallRule

#### Encryption
- cipher, BitLocker cmdlets, Protect-CmsMessage
- ConvertTo-SecureString, Get-Credential

</details>

### 6️⃣ Registry & Configuration (70+ commands)

<details>
<summary>Click to expand</summary>

#### Registry Operations
- reg query, reg add, reg delete, reg import, reg export
- Get-ItemProperty, Set-ItemProperty, New-ItemProperty
- Remove-ItemProperty, Test-Path

#### System Configuration
- sconfig, bcdedit, msconfig, regedit
- Get-ItemPropertyValue, Set-ItemPropertyValue

</details>

### 7️⃣ Performance & Monitoring (90+ commands)

<details>
<summary>Click to expand</summary>

#### Monitoring
- perfmon, resmon, taskmgr, Get-Counter
- Get-EventLog, Get-WinEvent, Get-EventSubscriber

#### Resource Management
- tasklist, taskkill, Get-Process, Stop-Process
- Get-WmiObject Win32_Processor, Get-CimInstance

#### Diagnostics
- systeminfo, msinfo32, dxdiag, winsat
- Get-ComputerInfo, Test-ComputerSecureChannel

</details>

### 8️⃣ Scripting & Automation (120+ commands)

<details>
<summary>Click to expand</summary>

#### Script Development
- Variables, Functions, Loops, Conditions
- Error Handling, Try-Catch-Finally
- Script Blocks, Modules, Functions

#### Task Scheduling
- schtasks, Get-ScheduledTask, Register-ScheduledTask
- New-ScheduledTaskAction, New-ScheduledTaskTrigger

#### Advanced Scripting
- Invoke-Expression, Invoke-Command
- Start-Job, Get-Job, Receive-Job, Wait-Job

</details>

### 9️⃣ Cloud & DevOps Tools (70+ commands)

<details>
<summary>Click to expand</summary>

#### AWS CLI
- aws configure, aws s3, aws ec2, aws iam
- aws cloudformation, aws lambda, aws rds

#### Azure CLI  
- az login, az account, az vm, az storage
- az network, az group, az webapp

#### Docker & Kubernetes
- docker run, docker ps, docker build, docker compose
- kubectl get, kubectl apply, kubectl delete

</details>

---

## 📊 Command Statistics

| Level | Commands | Percentage |
|-------|----------|------------|
| 🟢 Basic | 150 | 15% |
| 🟡 Intermediate | 250 | 25% |
| 🟠 Advanced | 300 | 30% |
| 🔴 Professional | 200 | 20% |
| ⚫ Expert | 100 | 10% |
| **Total** | **1000+** | **100%** |

---

## 🔍 Search & Find Commands

### Quick Command Lookup

```powershell
# Find commands by keyword
Get-Command *network*
Get-Command *service*
Get-Command *process*

# Get command help
Get-Help <command> -Full
Get-Help <command> -Examples
Get-Help <command> -Online

# Find command aliases
Get-Alias
Get-Alias -Definition Get-ChildItem
```

---

## 💼 Professional Use Cases

### 1. System Administration
- User and group management
- Service control and monitoring
- System configuration and optimization
- Security and access control

### 2. Network Administration
- Network configuration and diagnostics
- Remote system management
- Firewall and security policies
- VPN and connectivity troubleshooting

### 3. DevOps & Automation
- Infrastructure as Code
- CI/CD pipeline integration
- Container and orchestration management
- Cloud resource provisioning

### 4. Security Operations
- Security auditing and compliance
- Threat detection and response
- Access control and permissions
- Encryption and data protection

---

## 📚 Additional Resources

### Official Documentation
- [Microsoft Docs - PowerShell](https://docs.microsoft.com/powershell/)
- [Microsoft Docs - Windows Commands](https://docs.microsoft.com/windows-server/administration/windows-commands/)
- [PowerShell Gallery](https://www.powershellgallery.com/)

### Learning Resources
- [PowerShell in a Month of Lunches](https://www.manning.com/books/learn-windows-powershell-in-a-month-of-lunches)
- [Microsoft Learn](https://learn.microsoft.com/training/)
- [PowerShell.org](https://powershell.org/)

### Community
- [r/PowerShell](https://reddit.com/r/PowerShell)
- [Stack Overflow - PowerShell](https://stackoverflow.com/questions/tagged/powershell)
- [PowerShell Discord](https://discord.gg/powershell)

---

## 🚀 Getting Started

1. **Choose your level**: Start with [Basic Commands](01-system-file.md) if you're new
2. **Pick a category**: Navigate to the relevant section
3. **Practice**: Try commands in a test environment first
4. **Learn progressively**: Move from basic to advanced gradually
5. **Automate**: Create scripts for repetitive tasks

---

## ⚠️ Important Notes

### Safety Guidelines
- ⚠️ Always test commands in a non-production environment first
- 🔒 Many commands require administrator privileges
- 💾 Backup important data before making system changes
- 📝 Document your changes for future reference
- 🔄 Use `-WhatIf` parameter in PowerShell to preview changes

### Best Practices
- Use PowerShell for automation and scripting
- Learn to use help system effectively
- Understand command parameters and options
- Use aliases cautiously in scripts
- Follow naming conventions and standards

---

## 🆘 Troubleshooting

### Common Issues
1. **Execution Policy Errors**: `Set-ExecutionPolicy RemoteSigned`
2. **Permission Denied**: Run as Administrator
3. **Command Not Found**: Check PATH environment variable
4. **Module Not Loaded**: `Import-Module <ModuleName>`

### Getting Help
```powershell
# Command help
Get-Help <command>
Get-Help <command> -Examples
Get-Help <command> -Parameter *

# Find commands
Get-Command *keyword*
Get-Command -Module <ModuleName>

# Command history
Get-History
Invoke-History <id>
```

---

<div align="center">

## 🎓 Ready to Master Windows Commands?

**Start with:** [System & File Management →](01-system-file.md)

---

**Made with ❤️ by 0xff for AutoCloud**

[Back to Main Documentation](../../README.md)

</div>
