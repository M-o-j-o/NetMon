from ping3 import ping
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision

# InfluxDB config
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "9PEAb8NyeThtMIXAWmuEvteKJPH_BRlRACe2H8k1LePi7Qt0wZd-cirpW-s0uo5qPZa1hkfR06w_Q9nJ8CeUSQ=="
INFLUX_ORG = "mojosec"
INFLUX_BUCKET = "NetMon"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

# Devices to monitor
DEVICES = [
    {"name": "Google DNS", "ip": "8.8.8.8"},
    {"name": "Cloudflare DNS", "ip": "1.1.1.1"},
    {"name": "Local Router", "ip": "192.168.1.1"},
]

def check_device(device):
    try:
        response_time = ping(device["ip"], timeout=2)
        status = 1 if response_time else 0
        return status, round(response_time * 1000, 2) if response_time else None
    except Exception:
        return 0, None

def update_devices():
    for device in DEVICES:
        status, response_time = check_device(device)
        point = (
            Point("device_status")
            .tag("device", device["name"])
            .tag("ip", device["ip"])
            .field("status", status)
            .field("response_time", float(response_time) if response_time is not None else 0.0)
            .time(datetime.utcnow(), WritePrecision.NS)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
