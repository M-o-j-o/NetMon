#!/usr/bin/env python3
"""
Windows Monitoring Agent for Network Monitoring Dashboard
Collects system metrics and sends them to the dashboard
"""

import psutil
import requests
import time
import json
import socket
import platform
import os
from datetime import datetime

class WindowsMonitoringAgent:
    def __init__(self, dashboard_url, device_id, api_key=None):
        self.dashboard_url = dashboard_url.rstrip('/')
        self.device_id = device_id
        self.api_key = api_key
        self.hostname = socket.gethostname()
        self.interval = 30  # seconds
        
    def get_system_metrics(self):
        """Collect comprehensive system metrics for Windows"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk metrics (C: drive)
            disk = psutil.disk_usage('C:')
            disk_io = psutil.disk_io_counters()
            
            # Network metrics
            network = psutil.net_io_counters()
            
            # System info
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_days = int(uptime_seconds // 86400)
            uptime_hours = int((uptime_seconds % 86400) // 3600)
            uptime_minutes = int((uptime_seconds % 3600) // 60)
            
            # Windows-specific metrics
            try:
                import wmi
                c = wmi.WMI()
                
                # Get Windows version
                os_info = c.Win32_OperatingSystem()[0]
                windows_version = f"{os_info.Caption} {os_info.Version}"
                
                # Get CPU temperature (if available)
                cpu_temp = None
                try:
                    temp_info = c.MSAcpi_ThermalZoneTemperature()
                    if temp_info:
                        cpu_temp = round((temp_info[0].CurrentTemperature / 10.0) - 273.15, 1)
                except:
                    pass
                    
            except ImportError:
                windows_version = platform.platform()
                cpu_temp = None
            
            metrics = {
                'device_id': self.device_id,
                'hostname': self.hostname,
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': round(cpu_percent, 1),
                'cpu_count': cpu_count,
                'cpu_temperature': cpu_temp,
                'memory_usage': round(memory.percent, 1),
                'memory_total': memory.total,
                'memory_available': memory.available,
                'swap_usage': round(swap.percent, 1) if swap.total > 0 else 0,
                'disk_usage': round((disk.used / disk.total) * 100, 1),
                'disk_total': disk.total,
                'disk_free': disk.free,
                'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
                'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'network_packets_sent': network.packets_sent,
                'network_packets_recv': network.packets_recv,
                'uptime': f"{uptime_days}d {uptime_hours}h {uptime_minutes}m",
                'uptime_seconds': int(uptime_seconds),
                'platform': windows_version,
                'status': 'healthy'
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return {
                'device_id': self.device_id,
                'hostname': self.hostname,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def send_metrics(self, metrics):
        """Send metrics to dashboard"""
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            response = requests.post(
                f"{self.dashboard_url}/api/metrics/submit",
                json=metrics,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ Metrics sent successfully at {metrics['timestamp']}")
                return True
            else:
                print(f"✗ Failed to send metrics: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error sending metrics: {e}")
            return False
        except Exception as e:
            print(f"✗ Error sending metrics: {e}")
            return False
    
    def run(self):
        """Main monitoring loop"""
        print(f"Starting Windows Monitoring Agent for device {self.device_id}")
        print(f"Dashboard URL: {self.dashboard_url}")
        print(f"Hostname: {self.hostname}")
        print(f"Update interval: {self.interval} seconds")
        print("-" * 50)
        
        while True:
            try:
                metrics = self.get_system_metrics()
                self.send_metrics(metrics)
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                print("\n⚠ Monitoring agent stopped by user")
                break
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
                time.sleep(self.interval)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python monitoring_agent_windows.py <dashboard_url> <device_id> [api_key]")
        print("Example: python monitoring_agent_windows.py http://192.168.1.100:5000 1")
        sys.exit(1)
    
    dashboard_url = sys.argv[1]
    device_id = sys.argv[2]
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    agent = WindowsMonitoringAgent(dashboard_url, device_id, api_key)
    agent.run()
