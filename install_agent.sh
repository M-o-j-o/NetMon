#!/bin/bash
# Monitoring Agent Installation Script

echo "Installing Network Monitoring Agent..."

# Update package manager
sudo apt-get update -y

# Install Python and pip if not present
sudo apt-get install -y python3 python3-pip

# Install required Python packages
pip3 install psutil requests

# Create monitoring directory
sudo mkdir -p /opt/monitoring

# Copy agent script
sudo cp monitoring_agent.py /opt/monitoring/

# Make executable
sudo chmod +x /opt/monitoring/monitoring_agent.py

# Create systemd service
sudo tee /etc/systemd/system/monitoring-agent.service > /dev/null <<EOF
[Unit]
Description=Network Monitoring Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/monitoring_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable monitoring-agent
sudo systemctl start monitoring-agent

echo "Monitoring agent installed and started!"
echo "Check status with: sudo systemctl status monitoring-agent"
echo "View logs with: sudo journalctl -u monitoring-agent -f"
