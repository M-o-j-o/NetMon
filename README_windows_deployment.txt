Network Monitor Agent - Windows Deployment Guide
===============================================

STEP 1: Download Files
---------------------
Download these files to a folder on your Windows machine:
- monitoring_agent_windows.py
- install_windows_agent.ps1  
- deploy_windows.bat (this file)

STEP 2: Run Installation
-----------------------
1. Right-click on "deploy_windows.bat"
2. Select "Run as administrator"
3. Enter your dashboard URL (e.g., http://192.168.1.100:5000)
4. Enter a device ID (e.g., 1, 2, 3...)
5. Wait for installation to complete

STEP 3: Verify Installation
--------------------------
Open PowerShell as Administrator and run:
- Get-Service NetMonitorAgent
- Get-EventLog -LogName Application -Source NetMonitorAgent -Newest 5

TROUBLESHOOTING
--------------
If you get execution policy errors:
1. Open PowerShell as Administrator
2. Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
3. Try the installation again

Manual Installation:
1. Open PowerShell as Administrator
2. Navigate to the folder with the files: cd "C:\path\to\your\files"
3. Run: .\install_windows_agent.ps1 -DashboardUrl http://YOUR_IP:5000 -DeviceId 1

Service Management:
- Start-Service NetMonitorAgent
- Stop-Service NetMonitorAgent  
- Restart-Service NetMonitorAgent
- Get-Service NetMonitorAgent
