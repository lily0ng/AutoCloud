# Windows Command Templates

<div align="center">

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)
![CMD](https://img.shields.io/badge/CMD-4D4D4D?style=for-the-badge&logo=windows-terminal&logoColor=white)

**AutoCloud Windows Command Reference**

</div>

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [PowerShell Commands](#-powershell-commands)
- [CMD Commands](#-cmd-commands)
- [Terraform](#-terraform)
- [Docker](#-docker)
- [Kubernetes](#-kubernetes)
- [AWS CLI](#-aws-cli)
- [Azure CLI](#-azure-cli)
- [Git](#-git)

---

## 🔧 Prerequisites

### Check PowerShell Version
```powershell
$PSVersionTable.PSVersion
```

### Check CMD Version
```cmd
ver
```

### Install Chocolatey (Package Manager)
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Install Required Tools
```powershell
# Terraform
choco install terraform -y

# Docker Desktop
choco install docker-desktop -y

# Kubernetes CLI
choco install kubernetes-cli -y

# AWS CLI
choco install awscli -y

# Azure CLI
choco install azure-cli -y

# Git
choco install git -y

# Visual Studio Code
choco install vscode -y
```

---

## 💻 PowerShell Commands

### System Information
```powershell
# Display system information
Get-ComputerInfo | Select-Object CsName, WindowsVersion, OsArchitecture

# Check disk space
Get-PSDrive -PSProvider FileSystem

# Network configuration
Get-NetIPConfiguration

# Environment variables
Get-ChildItem Env:
```

### File Operations
```powershell
# Create directory
New-Item -ItemType Directory -Path "C:\AutoCloud\terraform"

# Copy files
Copy-Item -Path "source.tf" -Destination "C:\AutoCloud\terraform\"

# Move files
Move-Item -Path "source.tf" -Destination "C:\AutoCloud\terraform\"

# Delete files
Remove-Item -Path "file.txt" -Force

# Find files
Get-ChildItem -Path "C:\AutoCloud" -Recurse -Filter "*.tf"
```

### Process Management
```powershell
# List running processes
Get-Process

# Kill process by name
Stop-Process -Name "terraform" -Force

# Kill process by ID
Stop-Process -Id 1234 -Force
```

---

## 📟 CMD Commands

### Basic Navigation
```cmd
:: Change directory
cd C:\AutoCloud

:: Create directory
mkdir terraform

:: List files
dir

:: Copy files
copy source.tf destination.tf

:: Delete files
del file.txt

:: Move files
move source.tf C:\AutoCloud\terraform\
```

### Network Commands
```cmd
:: Check connectivity
ping google.com

:: Display network configuration
ipconfig /all

:: Flush DNS cache
ipconfig /flushdns

:: Trace route
tracert google.com
```

---

## 🏗️ Terraform

### Installation Verification
```powershell
terraform --version
```

### Initialize Project
```powershell
# Navigate to project directory
cd C:\AutoCloud\terraform\aws

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt
```

### Plan and Apply
```powershell
# Create execution plan
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Auto-approve (use with caution)
terraform apply -auto-approve

# Show current state
terraform show

# List resources
terraform state list
```

### Destroy Resources
```powershell
# Destroy all resources
terraform destroy

# Destroy specific resource
terraform destroy -target=aws_instance.example
```

### Workspaces
```powershell
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new dev

# Switch workspace
terraform workspace select dev

# Delete workspace
terraform workspace delete dev
```

---

## 🐳 Docker

### Docker Commands
```powershell
# Check Docker version
docker --version

# List running containers
docker ps

# List all containers
docker ps -a

# Pull image
docker pull nginx:latest

# Run container
docker run -d -p 80:80 --name web nginx:latest

# Stop container
docker stop web

# Remove container
docker rm web

# List images
docker images

# Remove image
docker rmi nginx:latest

# Build image
docker build -t myapp:latest .

# View container logs
docker logs web

# Execute command in container
docker exec -it web /bin/bash
```

### Docker Compose
```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build
```

---

## ☸️ Kubernetes

### Kubectl Commands
```powershell
# Check version
kubectl version --client

# Get cluster info
kubectl cluster-info

# Get nodes
kubectl get nodes

# Get pods
kubectl get pods -A

# Get services
kubectl get svc -A

# Get deployments
kubectl get deployments -A

# Describe resource
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Apply configuration
kubectl apply -f deployment.yaml

# Delete resource
kubectl delete -f deployment.yaml

# Port forward
kubectl port-forward pod/<pod-name> 8080:80
```

### Namespace Management
```powershell
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace dev

# Delete namespace
kubectl delete namespace dev

# Set default namespace
kubectl config set-context --current --namespace=dev
```

---

## ☁️ AWS CLI

### Configuration
```powershell
# Configure AWS CLI
aws configure

# Set profile
aws configure --profile dev

# List profiles
Get-Content $env:USERPROFILE\.aws\credentials
```

### EC2 Commands
```powershell
# List instances
aws ec2 describe-instances --region us-east-1

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### S3 Commands
```powershell
# List buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-bucket-name

# Upload file
aws s3 cp file.txt s3://my-bucket-name/

# Download file
aws s3 cp s3://my-bucket-name/file.txt .

# Sync directory
aws s3 sync ./local-dir s3://my-bucket-name/

# Delete bucket
aws s3 rb s3://my-bucket-name --force
```

---

## 🔷 Azure CLI

### Login and Configuration
```powershell
# Login to Azure
az login

# Set subscription
az account set --subscription "subscription-id"

# List subscriptions
az account list --output table
```

### Resource Group Commands
```powershell
# Create resource group
az group create --name MyResourceGroup --location eastus

# List resource groups
az group list --output table

# Delete resource group
az group delete --name MyResourceGroup --yes
```

### VM Commands
```powershell
# Create VM
az vm create --resource-group MyResourceGroup --name MyVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys

# List VMs
az vm list --output table

# Start VM
az vm start --resource-group MyResourceGroup --name MyVM

# Stop VM
az vm stop --resource-group MyResourceGroup --name MyVM

# Delete VM
az vm delete --resource-group MyResourceGroup --name MyVM --yes
```

---

## 📦 Git

### Basic Commands
```powershell
# Clone repository
git clone https://github.com/0xff/autocloud.git

# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Add new feature"

# Push changes
git push origin main

# Pull changes
git pull origin main

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# Merge branch
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

### Advanced Commands
```powershell
# View commit history
git log --oneline --graph --all

# Stash changes
git stash save "Work in progress"

# Apply stash
git stash pop

# Reset changes
git reset --hard HEAD

# Cherry-pick commit
git cherry-pick <commit-hash>

# Rebase
git rebase main
```

---

## 🔐 Environment Variables

### Set Environment Variables (PowerShell)
```powershell
# Temporary (current session)
$env:AWS_ACCESS_KEY_ID = "your-access-key"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-key"
$env:AWS_REGION = "us-east-1"

# Permanent (user level)
[System.Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "your-access-key", "User")

# Permanent (system level - requires admin)
[System.Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "your-access-key", "Machine")
```

### Set Environment Variables (CMD)
```cmd
:: Temporary (current session)
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_REGION=us-east-1

:: Permanent (user level)
setx AWS_ACCESS_KEY_ID "your-access-key"
```

---

## 📝 Useful Scripts

### PowerShell: Check All Prerequisites
```powershell
# check-prerequisites.ps1
Write-Host "Checking AutoCloud Prerequisites..." -ForegroundColor Cyan

# Check Terraform
try {
    $tfVersion = terraform --version
    Write-Host "✓ Terraform installed: $($tfVersion -split '\n')[0]" -ForegroundColor Green
} catch {
    Write-Host "✗ Terraform not found" -ForegroundColor Red
}

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found" -ForegroundColor Red
}

# Check Kubernetes
try {
    $kubectlVersion = kubectl version --client --short
    Write-Host "✓ Kubectl installed: $kubectlVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Kubectl not found" -ForegroundColor Red
}

# Check AWS CLI
try {
    $awsVersion = aws --version
    Write-Host "✓ AWS CLI installed: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ AWS CLI not found" -ForegroundColor Red
}

# Check Azure CLI
try {
    $azVersion = az --version | Select-Object -First 1
    Write-Host "✓ Azure CLI installed: $azVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Azure CLI not found" -ForegroundColor Red
}
```

---

## 🆘 Troubleshooting

### PowerShell Execution Policy
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Set policy for local machine (requires admin)
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned
```

### Path Issues
```powershell
# View PATH
$env:Path -split ';'

# Add to PATH temporarily
$env:Path += ";C:\Program Files\Terraform"

# Add to PATH permanently (user)
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Terraform", "User")
```

---

<div align="center">

**Made with ❤️ by 0xff**

[Back to Main Documentation](../../README.md)

</div>
