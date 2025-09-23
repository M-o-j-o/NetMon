from flask import Flask, render_template, jsonify, request
import requests
import json
import time
from datetime import datetime, timedelta
import random
import sqlite3
import os

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
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM devices')
    if cursor.fetchone()[0] == 0:
        sample_devices = [
            ('Web Server 01', '192.168.1.10', 'server', 22, 'Primary web server', 'web,production'),
            ('Database Server', '192.168.1.20', 'server', 22, 'Main database server', 'database,production'),
            ('Load Balancer', '192.168.1.5', 'network', 80, 'HAProxy load balancer', 'network,loadbalancer'),
            ('Cache Server', '192.168.1.30', 'server', 22, 'Redis cache server', 'cache,redis'),
            ('Backup Server', '192.168.1.40', 'server', 22, 'Backup and archive server', 'backup,storage'),
        ]
        
        cursor.executemany('''
            INSERT INTO devices (name, ip_address, device_type, port, description, tags)
            VALUES (?, ?, ?, ?, ?, ?)
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
            'created_at': row[7],
            'updated_at': row[8],
            'enabled': row[9],
            'status': row[10] or 'unknown',
            'response_time': row[11] or 0,
            'last_seen': row[12]
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
    """Main dashboard page"""
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
