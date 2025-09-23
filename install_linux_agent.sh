#!/bin/bash
# Linux Agent Installation Script for Network Monitoring Dashboard

set -e

DASHBOARD_URL=""
DEVICE_ID=""
API_KEY=""
INSTALL_DIR="/opt/netmonitor"
SERVICE_NAME="netmonitor-agent"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

install_dependencies() {
    print_status "Installing dependencies..."
    
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y python3 python3-pip curl
    elif command -v yum &> /dev/null; then
        yum update -y
        yum install -y python3 python3-pip curl
    elif command -v dnf &> /dev/null; then
        dnf update -y
        dnf install -y python3 python3-pip curl
    else
        print_error "Unsupported package manager. Please install Python 3 and pip manually."
        exit 1
    fi
    
    pip3 install psutil requests
}

create_directories() {
    print_status "Creating installation directories..."
    mkdir -p $INSTALL_DIR
    mkdir -p /var/log/netmonitor
}

install_agent() {
    print_status "Installing monitoring agent..."
    
    # Download or copy the agent script
    if [[ -f "monitoring_agent_linux.py" ]]; then
        cp monitoring_agent_linux.py $INSTALL_DIR/
    else
        print_error "monitoring_agent_linux.py not found in current directory"
        exit 1
    fi
    
    chmod +x $INSTALL_DIR/monitoring_agent_linux.py
    
    # Create configuration file
    cat > $INSTALL_DIR/config.json << EOF
{
    "dashboard_url": "$DASHBOARD_URL",
    "device_id": "$DEVICE_ID",
    "api_key": "$API_KEY",
    "interval": 30,
    "log_level": "INFO"
}
EOF
}

create_systemd_service() {
    print_status "Creating systemd service..."
    
    cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Network Monitor Agent
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/monitoring_agent_linux.py $DASHBOARD_URL $DEVICE_ID $API_KEY
Restart=always
RestartSec=10
StandardOutput=append:/var/log/netmonitor/agent.log
StandardError=append:/var/log/netmonitor/agent.log

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
}

start_service() {
    print_status "Starting monitoring agent service..."
    systemctl start $SERVICE_NAME
    
    sleep 3
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        print_status "✓ Monitoring agent started successfully!"
        print_status "Service status: $(systemctl is-active $SERVICE_NAME)"
    else
        print_error "✗ Failed to start monitoring agent"
        print_error "Check logs: journalctl -u $SERVICE_NAME -f"
        exit 1
    fi
}

show_usage() {
    echo "Usage: $0 <dashboard_url> <device_id> [api_key]"
    echo ""
    echo "Examples:"
    echo "  $0 http://192.168.1.100:5000 1"
    echo "  $0 https://monitor.example.com 1 your-api-key"
    echo ""
    echo "Commands:"
    echo "  sudo systemctl status $SERVICE_NAME    # Check service status"
    echo "  sudo systemctl stop $SERVICE_NAME      # Stop service"
    echo "  sudo systemctl start $SERVICE_NAME     # Start service"
    echo "  sudo journalctl -u $SERVICE_NAME -f    # View logs"
    exit 1
}

main() {
    if [[ $# -lt 2 ]]; then
        show_usage
    fi
    
    DASHBOARD_URL="$1"
    DEVICE_ID="$2"
    API_KEY="${3:-}"
    
    print_status "Installing Network Monitor Agent..."
    print_status "Dashboard URL: $DASHBOARD_URL"
    print_status "Device ID: $DEVICE_ID"
    
    check_root
    install_dependencies
    create_directories
    install_agent
    create_systemd_service
    start_service
    
    print_status ""
    print_status "✓ Installation completed successfully!"
    print_status ""
    print_status "Useful commands:"
    print_status "  sudo systemctl status $SERVICE_NAME    # Check service status"
    print_status "  sudo systemctl restart $SERVICE_NAME   # Restart service"
    print_status "  sudo journalctl -u $SERVICE_NAME -f    # View live logs"
    print_status "  tail -f /var/log/netmonitor/agent.log  # View agent logs"
}

main "$@"
