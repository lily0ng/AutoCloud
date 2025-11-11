# Windows Setup Script for Cloud Monitoring

# Function to detect cloud provider
function Detect-CloudProvider {
    try {
        # Check AWS
        $awsMetadata = Invoke-WebRequest -Uri "http://169.254.169.254/latest/meta-data/" -TimeoutSec 5
        if ($?) { return "aws" }
    } catch {}
    
    try {
        # Check Azure
        $azureMetadata = Invoke-WebRequest -Uri "http://169.254.169.254/metadata/instance?api-version=2021-02-01" -Headers @{"Metadata"="true"} -TimeoutSec 5
        if ($?) { return "azure" }
    } catch {}
    
    try {
        # Check GCP
        $gcpMetadata = Invoke-WebRequest -Uri "http://metadata.google.internal/computeMetadata/v1/" -Headers @{"Metadata-Flavor"="Google"} -TimeoutSec 5
        if ($?) { return "gcp" }
    } catch {}
    
    return "unknown"
}

# Function to install AWS CloudWatch Agent
function Install-AWSCloudWatchAgent {
    # Download CloudWatch Agent
    $installerPath = "$env:TEMP\AmazonCloudWatchAgent.msi"
    Invoke-WebRequest -Uri "https://s3.amazonaws.com/amazoncloudwatch-agent/windows/amd64/latest/amazon-cloudwatch-agent.msi" -OutFile $installerPath
    
    # Install CloudWatch Agent
    Start-Process msiexec.exe -Wait -ArgumentList "/i $installerPath /qn"
    
    # Copy configuration
    Copy-Item "..\configs\aws\cloudwatch-agent.json" -Destination "$env:ProgramData\Amazon\AmazonCloudWatchAgent\config.json"
    
    # Start the agent
    & "$env:ProgramFiles\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a fetch-config -m ec2 -s -c file:"$env:ProgramData\Amazon\AmazonCloudWatchAgent\config.json"
}

# Function to install Azure Monitor Agent
function Install-AzureMonitorAgent {
    # Download Azure Monitor Agent
    Invoke-WebRequest -Uri "https://aka.ms/amagentwin" -OutFile "$env:TEMP\AzureMonitorAgent.msi"
    
    # Install Azure Monitor Agent
    Start-Process msiexec.exe -Wait -ArgumentList "/i $env:TEMP\AzureMonitorAgent.msi /qn"
    
    # Copy configuration
    Copy-Item "..\configs\azure\monitoring-config.json" -Destination "$env:ProgramData\Microsoft\Azure\Monitor\Config\monitoring-config.json"
    
    # Restart the service
    Restart-Service "Azure Monitor Agent"
}

# Function to install Google Cloud Operations Agent
function Install-GCPOperationsAgent {
    # Download and install the agent
    (New-Object Net.WebClient).DownloadFile("https://dl.google.com/cloudagents/windows/StackdriverMonitoring.exe", "$env:TEMP\StackdriverMonitoring.exe")
    Start-Process -Wait -FilePath "$env:TEMP\StackdriverMonitoring.exe" -ArgumentList "/S"
    
    # Copy configuration
    Copy-Item "..\configs\gcp\monitoring-config.yaml" -Destination "C:\Program Files\Google\Cloud Operations\config.yaml"
    
    # Restart the service
    Restart-Service "Google Cloud Operations"
}

# Main setup logic
$cloudProvider = Detect-CloudProvider

# Install common tools
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module -Name AWS.Tools.Common -Force
Install-Module -Name Az.Monitor -Force
Install-Module -Name GoogleCloud -Force

switch ($cloudProvider) {
    "aws" { Install-AWSCloudWatchAgent }
    "azure" { Install-AzureMonitorAgent }
    "gcp" { Install-GCPOperationsAgent }
    default { Write-Host "Unknown cloud provider or running on-premises" }
}

Write-Host "Monitoring agent setup complete for $cloudProvider"
