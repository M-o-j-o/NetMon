@echo off
echo Network Monitor Agent - Windows Deployment
echo ==========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Check if files exist
if not exist "monitoring_agent_windows.py" (
    echo ERROR: monitoring_agent_windows.py not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

if not exist "install_windows_agent.ps1" (
    echo ERROR: install_windows_agent.ps1 not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

REM Get dashboard URL and device ID from user
set /p DASHBOARD_URL="Enter Dashboard URL (e.g., http://192.168.1.100:5000): "
set /p DEVICE_ID="Enter Device ID (e.g., 1): "

echo.
echo Installing with:
echo Dashboard URL: %DASHBOARD_URL%
echo Device ID: %DEVICE_ID%
echo.

REM Set execution policy temporarily and run PowerShell script
powershell -ExecutionPolicy Bypass -File "install_windows_agent.ps1" -DashboardUrl "%DASHBOARD_URL%" -DeviceId "%DEVICE_ID%"

if %errorLevel% equ 0 (
    echo.
    echo ✓ Installation completed successfully!
    echo The monitoring agent is now running as a Windows service.
) else (
    echo.
    echo ✗ Installation failed. Check the error messages above.
)

pause
