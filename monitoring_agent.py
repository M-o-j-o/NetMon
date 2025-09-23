#!/usr/bin/env python3
"""
Network Monitoring Agent
Collects system metrics and sends them to the monitoring dashboard
"""

import json
import time
import psutil
import requests
import socket
import logging
from datetime import datetime
import sys
import os

# Configuration
DASHBOARD_URL = "http://YOUR_DASHBOARD_IP:5000"  # Update this
AGENT_ID = socket.gethostname()
COLLECTION_INTERVAL = 30  # seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/monitoring_agent.log'),
        logging.StreamHandler()
    ]
)

class MonitoringAgent:
    def __init__(self):
        self.dashboard_url = DASHBOARD_URL
        self.agent_id = AGENT_ID
        self.session = requests.Session()
        
    def collect_metrics(self):
        """Collect system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics
            network = psutil.net_io_counters()
            
            # System info
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            metrics = {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'system': {
                    'boot_time': boot_time.isoformat(),
                    'hostname': socket.gethostname()
                }
            }
            
            return metrics
            
        except Exception as e:
            logging.error(f"Error collecting metrics: {e}")
            return None
    
    def send_metrics(self, metrics):
        """Send metrics to dashboard"""
        try:
            response = self.session.post(
                f"{self.dashboard_url}/api/metrics",
                json=metrics,
                timeout=10
            )
            
            if response.status_code == 200:
                logging.info(f"Metrics sent successfully for {self.agent_id}")
                return True
            else:
                logging.error(f"Failed to send metrics: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error sending metrics: {e}")
            return False
    
    def register_agent(self):
        """Register this agent with the dashboard"""
        try:
            agent_info = {
                'agent_id': self.agent_id,
                'hostname': socket.gethostname(),
                'ip_address': socket.gethostbyname(socket.gethostname()),
                'platform': sys.platform,
                'registration_time': datetime.now().isoformat()
            }
            
            response = self.session.post(
                f"{self.dashboard_url}/api/register_agent",
                json=agent_info,
                timeout=10
            )
            
            if response.status_code == 200:
                logging.info(f"Agent {self.agent_id} registered successfully")
                return True
            else:
                logging.error(f"Failed to register agent: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error registering agent: {e}")
            return False
    
    def run(self):
        """Main monitoring loop"""
        logging.info(f"Starting monitoring agent for {self.agent_id}")
        
        # Register with dashboard
        self.register_agent()
        
        while True:
            try:
                # Collect metrics
                metrics = self.collect_metrics()
                
                if metrics:
                    # Send to dashboard
                    self.send_metrics(metrics)
                
                # Wait for next collection
                time.sleep(COLLECTION_INTERVAL)
                
            except KeyboardInterrupt:
                logging.info("Monitoring agent stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    # Install required packages if not present
    try:
        import psutil
        import requests
    except ImportError:
        logging.info("Installing required packages...")
        os.system("pip3 install psutil requests")
        import psutil
        import requests
    
    agent = MonitoringAgent()
    agent.run()
