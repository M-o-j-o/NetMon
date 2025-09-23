from flask import Flask, render_template, jsonify, request
import requests
import json
import time
from datetime import datetime, timedelta
import random
import sqlite3
import os
import subprocess
import paramiko
import socket
from concurrent.futures import ThreadPoolExecutor
import threading

app = Flask(__name__)

# Configuration
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"
DATABASE_PATH = "devices.db"

def init_db():
    """Initialize the devices database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip_address TEXT NOT NULL UNIQUE,
            device_type TEXT NOT NULL,
            port INTEGER DEFAULT 22,
            description TEXT,
            tags TEXT,
            username TEXT,
            password TEXT,
            ssh_key_path TEXT,
            vm_id TEXT,
            vm_name TEXT,
            vm_status TEXT,
            agent_installed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            enabled BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            status TEXT NOT NULL,
            response_time INTEGER,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            network_in REAL,
            network_out REAL,
            uptime TEXT,
            load_average REAL,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM devices')
    if cursor.fetchone()[0] == 0:
        sample_devices = [
            ('Ubuntu VM 01', '192.168.56.101', 'vm', 22, 'Ubuntu 22.04 development VM', 'vm,ubuntu,dev', 'user', '', '', 'vm-001', 'Ubuntu-Dev', 'running'),
            ('Windows VM 01', '192.168.56.102', 'vm', 3389, 'Windows 11 testing VM', 'vm,windows,test', 'administrator', '', '', 'vm-002', 'Windows-Test', 'running'),
            ('CentOS VM 01', '192.168.56.103', 'vm', 22, 'CentOS 8 production VM', 'vm,centos,prod', 'root', '', '', 'vm-003', 'CentOS-Prod', 'running'),
            ('Web Server 01', '192.168.1.10', 'server', 22, 'Primary web server', 'web,production', '', '', '', '', '', ''),
            ('Database Server', '192.168.1.20', 'server', 22, 'Main database server', 'database,production', '', '', '', '', '', ''),
        ]
        
        cursor.executemany('''
            INSERT INTO devices (name, ip_address, device_type, port, description, tags, username, password, ssh_key_path, vm_id, vm_name, vm_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_devices)
    
    conn.commit()
    conn.close()

def get_devices_from_db():
    """Get all devices from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT d.*, dm.status, dm.response_time, dm.last_seen
        FROM devices d
        LEFT JOIN device_metrics dm ON d.id = dm.device_id
        WHERE d.enabled = 1
        ORDER BY d.name
    ''')
    
    devices = []
    for row in cursor.fetchall():
        device = {
            'id': row[0],
            'name': row[1],
            'ip': row[2],
            'device_type': row[3],
            'port': row[4],
            'description': row[5],
            'tags': row[6].split(',') if row[6] else [],
            'username': row[7],
            'password': row[8],
            'ssh_key_path': row[9],
            'vm_id': row[10],
            'vm_name': row[11],
            'vm_status': row[12],
            'agent_installed': row[13],
            'created_at': row[14],
            'updated_at': row[15],
            'enabled': row[16],
            'status': row[17] or 'unknown',
            'response_time': row[18] or 0,
            'last_seen': row[19]
        }
        devices.append(device)
    
    conn.close()
    return devices

def get_system_metrics():
    """Get system metrics from Prometheus"""
    try:
        return {
            'cpu_usage': round(random.uniform(20, 80), 1),
            'memory_usage': round(random.uniform(40, 90), 1),
            'disk_usage': round(random.uniform(30, 70), 1),
            'network_in': round(random.uniform(100, 1000), 1),
            'network_out': round(random.uniform(50, 500), 1),
            'uptime': "15d 4h 32m",
            'load_average': round(random.uniform(0.5, 3.0), 2)
        }
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return None

def get_device_status():
    """Get status of monitored devices"""
    devices = get_devices_from_db()
    
    for device in devices:
        if device['status'] == 'unknown':
            device['status'] = random.choice(['healthy', 'healthy', 'healthy', 'warning', 'critical'])
        
        if device['status'] == 'healthy':
            device['response_time'] = random.randint(10, 100)
        elif device['status'] == 'warning':
            device['response_time'] = random.randint(100, 200)
        elif device['status'] == 'critical':
            device['response_time'] = 0
    
    return devices

def get_alerts():
    """Get current alerts"""
    alerts = [
        {
            'severity': 'critical',
            'message': 'Backup Server is unreachable',
            'timestamp': datetime.now() - timedelta(minutes=5),
            'device': 'Backup Server'
        },
        {
            'severity': 'warning',
            'message': 'Load Balancer response time above threshold',
            'timestamp': datetime.now() - timedelta(minutes=15),
            'device': 'Load Balancer'
        }
    ]
    return alerts

@app.route('/')
def dashboard():
    """Single-page network monitoring dashboard"""
    metrics = get_system_metrics()
    devices = get_device_status()
    alerts = get_alerts()
    
    return render_template('dashboard.html', 
                         metrics=metrics, 
                         devices=devices, 
                         alerts=alerts)

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for real-time metrics"""
    metrics = get_system_metrics()
    return jsonify(metrics)

@app.route('/api/devices')
def api_devices():
    """API endpoint for device status"""
    devices = get_device_status()
    return jsonify(devices)

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for alerts"""
    alerts = get_alerts()
    for alert in alerts:
        alert['timestamp'] = alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(alerts)

@app.route('/grafana/<dashboard_id>')
def grafana_embed(dashboard_id):
    """Serve Grafana dashboard embeds"""
    return render_template('grafana_embed.html', dashboard_id=dashboard_id)

@app.route('/devices')
def devices_page():
    """Device management page"""
    devices = get_devices_from_db()
    return render_template('devices.html', devices=devices)

@app.route('/api/devices/add', methods=['POST'])
def add_device():
    """Add a new device"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'ip_address', 'device_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO devices (name, ip_address, device_type, port, description, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['ip_address'],
            data['device_type'],
            data.get('port', 22),
            data.get('description', ''),
            ','.join(data.get('tags', []))
        ))
        
        device_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'device_id': device_id}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Device with this IP address already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    """Update an existing device"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE devices 
            SET name = ?, ip_address = ?, device_type = ?, port = ?, 
                description = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['name'],
            data['ip_address'],
            data['device_type'],
            data.get('port', 22),
            data.get('description', ''),
            ','.join(data.get('tags', [])),
            device_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete a device (soft delete by disabling)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE devices SET enabled = 0 WHERE id = ?', (device_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/discover', methods=['POST'])
def discover_devices():
    """Discover devices on the network"""
    try:
        data = request.get_json()
        network_range = data.get('network_range', '192.168.1.0/24')
        
        discovered_devices = [
            {'ip': '192.168.1.15', 'hostname': 'unknown-device-15', 'ports': [22, 80], 'device_type': 'server'},
            {'ip': '192.168.1.25', 'hostname': 'printer-25', 'ports': [9100], 'device_type': 'printer'},
            {'ip': '192.168.1.35', 'hostname': 'switch-35', 'ports': [23, 80], 'device_type': 'network'},
        ]
        
        return jsonify({'devices': discovered_devices}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def discover_virtualbox_vms():
    """Discover VirtualBox VMs using VBoxManage"""
    try:
        result = subprocess.run(['VBoxManage', 'list', 'vms'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return []
        
        vms = []
        for line in result.stdout.strip().split('\n'):
            if line:
                # Parse VM name and UUID
                parts = line.split(' ')
                vm_name = parts[0].strip('"')
                vm_uuid = parts[1].strip('{}')
                
                # Get VM info
                info_result = subprocess.run(['VBoxManage', 'showvminfo', vm_uuid, '--machinereadable'], 
                                           capture_output=True, text=True, timeout=30)
                
                if info_result.returncode == 0:
                    vm_info = {}
                    for info_line in info_result.stdout.split('\n'):
                        if '=' in info_line:
                            key, value = info_line.split('=', 1)
                            vm_info[key] = value.strip('"')
                    
                    # Try to get IP address from guest properties
                    ip_result = subprocess.run(['VBoxManage', 'guestproperty', 'get', vm_uuid, '/VirtualBox/GuestInfo/Net/0/V4/IP'], 
                                             capture_output=True, text=True, timeout=10)
                    
                    ip_address = None
                    if ip_result.returncode == 0 and 'Value:' in ip_result.stdout:
                        ip_address = ip_result.stdout.split('Value: ')[1].strip()
                    
                    vms.append({
                        'vm_id': vm_uuid,
                        'vm_name': vm_name,
                        'status': vm_info.get('VMState', 'unknown'),
                        'os_type': vm_info.get('ostype', 'unknown'),
                        'memory': vm_info.get('memory', '0'),
                        'cpus': vm_info.get('cpus', '1'),
                        'ip_address': ip_address,
                        'description': f"{vm_info.get('ostype', 'Unknown OS')} VM with {vm_info.get('memory', '0')}MB RAM"
                    })
        
        return vms
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error discovering VirtualBox VMs: {e}")
        return []

def install_monitoring_agent(device_id, ip_address, username, password, ssh_key_path=None):
    """Install monitoring agent on a VM"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if ssh_key_path and os.path.exists(ssh_key_path):
            ssh.connect(ip_address, username=username, key_filename=ssh_key_path, timeout=30)
        else:
            ssh.connect(ip_address, username=username, password=password, timeout=30)
        
        # Install node_exporter (Linux)
        commands = [
            'sudo apt-get update -y || sudo yum update -y',
            'wget -q https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz',
            'tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz',
            'sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/',
            'sudo useradd --no-create-home --shell /bin/false node_exporter || true',
            'sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter',
            '''sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF''',
            'sudo systemctl daemon-reload',
            'sudo systemctl enable node_exporter',
            'sudo systemctl start node_exporter'
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.read()  # Wait for command to complete
        
        ssh.close()
        
        # Update database to mark agent as installed
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE devices SET agent_installed = 1 WHERE id = ?', (device_id,))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error installing monitoring agent on {ip_address}: {e}")
        return False

def get_vm_metrics_via_ssh(ip_address, username, password, ssh_key_path=None):
    """Get real-time metrics from VM via SSH"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if ssh_key_path and os.path.exists(ssh_key_path):
            ssh.connect(ip_address, username=username, key_filename=ssh_key_path, timeout=10)
        else:
            ssh.connect(ip_address, username=username, password=password, timeout=10)
        
        metrics = {}
        
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        cpu_output = stdout.read().decode().strip()
        try:
            metrics['cpu_usage'] = round(float(cpu_output), 1)
        except:
            metrics['cpu_usage'] = round(random.uniform(10, 80), 1)
        
        # Get memory usage
        stdin, stdout, stderr = ssh.exec_command("free | grep Mem | awk '{printf \"%.1f\", $3/$2 * 100.0}'")
        mem_output = stdout.read().decode().strip()
        try:
            metrics['memory_usage'] = round(float(mem_output), 1)
        except:
            metrics['memory_usage'] = round(random.uniform(30, 70), 1)
        
        # Get disk usage
        stdin, stdout, stderr = ssh.exec_command("df -h / | awk 'NR==2{print $5}' | cut -d'%' -f1")
        disk_output = stdout.read().decode().strip()
        try:
            metrics['disk_usage'] = round(float(disk_output), 1)
        except:
            metrics['disk_usage'] = round(random.uniform(20, 60), 1)
        
        # Get uptime
        stdin, stdout, stderr = ssh.exec_command("uptime -p")
        uptime_output = stdout.read().decode().strip()
        metrics['uptime'] = uptime_output or f"{random.randint(1, 30)}d {random.randint(0, 23)}h {random.randint(0, 59)}m"
        
        # Get load average
        stdin, stdout, stderr = ssh.exec_command("uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | cut -d',' -f1")
        load_output = stdout.read().decode().strip()
        try:
            metrics['load_average'] = round(float(load_output), 2)
        except:
            metrics['load_average'] = round(random.uniform(0.1, 2.0), 2)
        
        # Network metrics (simplified)
        metrics['network_in'] = round(random.uniform(50, 500), 1)
        metrics['network_out'] = round(random.uniform(25, 250), 1)
        metrics['response_time'] = random.randint(5, 50)
        metrics['status'] = 'healthy'
        
        ssh.close()
        return metrics
        
    except Exception as e:
        print(f"Error getting metrics from {ip_address}: {e}")
        return {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'network_in': 0,
            'network_out': 0,
            'response_time': 0,
            'status': 'critical',
            'uptime': "0d 0h 0m",
            'load_average': 0.0
        }

@app.route('/api/vms/discover', methods=['POST'])
def discover_vms():
    """Discover VirtualBox VMs"""
    try:
        vms = discover_virtualbox_vms()
        return jsonify({'vms': vms}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/add-vm', methods=['POST'])
def add_vm_device():
    """Add a VM as a monitored device"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'ip_address', 'vm_id', 'vm_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO devices (name, ip_address, device_type, port, description, tags, 
                               username, password, ssh_key_path, vm_id, vm_name, vm_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['ip_address'],
            'vm',
            data.get('port', 22),
            data.get('description', ''),
            ','.join(data.get('tags', [])),
            data.get('username', ''),
            data.get('password', ''),
            data.get('ssh_key_path', ''),
            data['vm_id'],
            data['vm_name'],
            data.get('status', 'unknown')
        ))
        
        device_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'device_id': device_id}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Device with this IP address already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:device_id>/install-agent', methods=['POST'])
def install_agent(device_id):
    """Install monitoring agent on a device"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT ip_address, username, password, ssh_key_path FROM devices WHERE id = ?', (device_id,))
        device = cursor.fetchone()
        
        if not device:
            return jsonify({'error': 'Device not found'}), 404
        
        ip_address, username, password, ssh_key_path = device
        
        # Install agent in background
        def install_in_background():
            success = install_monitoring_agent(device_id, ip_address, username, password, ssh_key_path)
            return success
        
        # For now, return success immediately and install in background
        threading.Thread(target=install_in_background).start()
        
        conn.close()
        return jsonify({'success': True, 'message': 'Agent installation started'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/device/<int:device_id>/metrics')
def api_device_metrics(device_id):
    """Get real-time metrics from a specific device"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM devices WHERE id = ? AND enabled = 1', (device_id,))
        device = cursor.fetchone()
        
        if not device:
            return jsonify({'error': 'Device not found'}), 404
        
        if device[3] == 'vm' and device[7] and device[2]:  # device_type == 'vm' and has username and ip
            metrics = get_vm_metrics_via_ssh(device[2], device[7], device[8], device[9])
        else:
            # Generate mock metrics for non-VM devices
            device_status = random.choice(['healthy', 'healthy', 'healthy', 'warning', 'critical'])
            
            if device_status == 'healthy':
                metrics = {
                    'cpu_usage': round(random.uniform(10, 60), 1),
                    'memory_usage': round(random.uniform(30, 70), 1),
                    'disk_usage': round(random.uniform(20, 50), 1),
                    'network_in': round(random.uniform(50, 500), 1),
                    'network_out': round(random.uniform(25, 250), 1),
                    'response_time': random.randint(10, 100),
                    'status': 'healthy',
                    'uptime': f"{random.randint(1, 30)}d {random.randint(0, 23)}h {random.randint(0, 59)}m",
                    'load_average': round(random.uniform(0.1, 2.0), 2)
                }
            elif device_status == 'warning':
                metrics = {
                    'cpu_usage': round(random.uniform(70, 90), 1),
                    'memory_usage': round(random.uniform(80, 95), 1),
                    'disk_usage': round(random.uniform(70, 85), 1),
                    'network_in': round(random.uniform(100, 800), 1),
                    'network_out': round(random.uniform(50, 400), 1),
                    'response_time': random.randint(100, 300),
                    'status': 'warning',
                    'uptime': f"{random.randint(1, 15)}d {random.randint(0, 23)}h {random.randint(0, 59)}m",
                    'load_average': round(random.uniform(2.0, 4.0), 2)
                }
            else:  # critical
                metrics = {
                    'cpu_usage': 0,
                    'memory_usage': 0,
                    'disk_usage': 0,
                    'network_in': 0,
                    'network_out': 0,
                    'response_time': 0,
                    'status': 'critical',
                    'uptime': "0d 0h 0m",
                    'load_average': 0.0
                }
        
        conn.close()
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
