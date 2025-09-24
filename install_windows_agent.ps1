# Windows Agent Installation Script for Network Monitoring Dashboard
param(
    [Parameter(Mandatory=$true)]
    [string]$DashboardUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$DeviceId,
    
    [Parameter(Mandatory=$false)]
    [string]$ApiKey = ""
)

$ErrorActionPreference = "Stop"

# Configuration
$InstallDir = "C:\Program Files\NetMonitor"
$ServiceName = "NetMonitorAgent"
$ServiceDisplayName = "Network Monitor Agent"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-Dependencies {
    Write-Status "Installing dependencies..."
    
    # Check if Python is installed
    try {
        $pythonVersion = python --version 2>&1
        Write-Status "Python found: $pythonVersion"
    }
    catch {
        Write-Error "Python 3 is required but not found. Please install Python 3.7+ from https://python.org"
        exit 1
    }
    
    # Install required Python packages
    Write-Status "Installing Python packages..."
    pip install psutil requests pywin32
    
    # Install WMI package for Windows-specific metrics
    try {
        pip install WMI
        Write-Status "WMI package installed for enhanced Windows metrics"
    }
    catch {
        Write-Warning "Could not install WMI package. Some Windows-specific metrics may not be available."
    }
}

function Create-Directories {
    Write-Status "Creating installation directories..."
    
    if (!(Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    
    if (!(Test-Path "C:\ProgramData\NetMonitor\Logs")) {
        New-Item -ItemType Directory -Path "C:\ProgramData\NetMonitor\Logs" -Force | Out-Null
    }
}

function Install-Agent {
    Write-Status "Installing monitoring agent..."
    
    # Check if agent script exists
    if (!(Test-Path "monitoring_agent_windows.py")) {
        Write-Error "monitoring_agent_windows.py not found in current directory"
        exit 1
    }
    
    # Copy agent script
    Copy-Item "monitoring_agent_windows.py" "$InstallDir\" -Force
    
    # Create configuration file
    $config = @{
        dashboard_url = $DashboardUrl
        device_id = $DeviceId
        api_key = $ApiKey
        interval = 30
        log_level = "INFO"
    } | ConvertTo-Json
    
    $config | Out-File "$InstallDir\config.json" -Encoding UTF8
    
    # Create wrapper script for service
    $wrapperScript = @'
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Import and run agent
from monitoring_agent_windows import WindowsMonitoringAgent

agent = WindowsMonitoringAgent(
    config['dashboard_url'],
    config['device_id'],
    config.get('api_key')
)

agent.run()
'@
    
    $wrapperScript | Out-File "$InstallDir\service_wrapper.py" -Encoding UTF8
}

function Install-Service {
    Write-Status "Installing Windows service..."
    
    # Create service installation script
    $serviceScript = @'
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess
import time

class NetMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "{0}"
    _svc_display_name_ = "{1}"
    _svc_description_ = "Collects system metrics and sends them to the network monitoring dashboard"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.process = None
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()
    
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.main()
    
    def main(self):
        while True:
            try:
                # Run the monitoring agent
                script_path = os.path.join(r"{2}", "service_wrapper.py")
                self.process = subprocess.Popen([sys.executable, script_path])
                
                # Wait for stop event or process to finish
                while True:
                    if win32event.WaitForSingleObject(self.hWaitStop, 1000) == win32event.WAIT_OBJECT_0:
                        break
                    if self.process.poll() is not None:
                        # Process died, restart it
                        time.sleep(5)
                        break
                        
            except Exception as e:
                servicemanager.LogErrorMsg(f"Service error: {str(e)}")
                time.sleep(10)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(NetMonitorService)
'@ -f $ServiceName, $ServiceDisplayName, $InstallDir
    
    $serviceScript | Out-File "$InstallDir\service.py" -Encoding UTF8
    
    # Install the service
    try {
        & python "$InstallDir\service.py" install
        Write-Status "Service installed successfully"
    }
    catch {
        Write-Error "Failed to install service: $_"
        exit 1
    }
}

function Start-AgentService {
    Write-Status "Starting monitoring agent service..."
    
    try {
        Start-Service $ServiceName
        Start-Sleep 3
        
        $service = Get-Service $ServiceName
        if ($service.Status -eq "Running") {
            Write-Status "✓ Monitoring agent started successfully!"
            Write-Status "Service status: $($service.Status)"
        }
        else {
            Write-Error "✗ Failed to start monitoring agent"
            Write-Error "Check Windows Event Log for details"
            exit 1
        }
    }
    catch {
        Write-Error "Failed to start service: $_"
        exit 1
    }
}

function Show-Usage {
    Write-Host ""
    Write-Host "Usage: .\install_windows_agent.ps1 -DashboardUrl 'url' -DeviceId 'id' [-ApiKey 'key']"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\install_windows_agent.ps1 -DashboardUrl http://192.168.1.100:5000 -DeviceId 1"
    Write-Host "  .\install_windows_agent.ps1 -DashboardUrl https://monitor.example.com -DeviceId 1 -ApiKey your-api-key"
    Write-Host ""
    Write-Host "Service Management:"
    Write-Host "  Get-Service $ServiceName                    # Check service status"
    Write-Host "  Stop-Service $ServiceName                   # Stop service"
    Write-Host "  Start-Service $ServiceName                  # Start service"
    Write-Host "  Get-EventLog -LogName Application -Source $ServiceName  # View logs"
    exit 1
}

# Main execution
try {
    if (-not (Test-Administrator)) {
        Write-Error "This script must be run as Administrator"
        exit 1
    }
    
    Write-Status "Installing Network Monitor Agent for Windows..."
    Write-Status "Dashboard URL: $DashboardUrl"
    Write-Status "Device ID: $DeviceId"
    
    Install-Dependencies
    Create-Directories
    Install-Agent
    Install-Service
    Start-AgentService
    
    Write-Status ""
    Write-Status "✓ Installation completed successfully!"
    Write-Status ""
    Write-Status "Useful commands:"
    Write-Status "  Get-Service $ServiceName                    # Check service status"
    Write-Status "  Restart-Service $ServiceName                # Restart service"
    Write-Status "  Get-EventLog -LogName Application -Source $ServiceName -Newest 10  # View recent logs"
}
catch {
    Write-Error "Installation failed: $_"
    exit 1
}