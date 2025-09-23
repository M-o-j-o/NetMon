# NetMon

NetMon is a simple yet powerful network monitoring tool built with Python (Flask) for the backend, Prometheus for metrics collection, and Grafana for visualization. It tracks device availability (ping, up/down), response times, and provides real-time insights into network health. NetMon is designed to be easy to deploy and extend, supporting both Windows and Linux environments.

---

## Features

- **Device Discovery:** Add and manage network devices (Linux, Windows, VMs, servers, workstations) via a web UI or API.
- **Real-Time Monitoring:** Tracks device status (up/down), response times, and system metrics.
- **Performance Graphs:** Visualizes CPU and memory usage with Chart.js and Grafana dashboards.
- **Prometheus Integration:** Collects metrics from Prometheus and Node Exporter.
- **Grafana Dashboards:** Embeds Grafana panels for advanced visualization.
- **Custom Alerts:** Status indicators for healthy, warning, and critical devices.
- **Responsive UI:** Modern dashboard built with Tailwind CSS and Font Awesome.
- **Multi-Platform Deployment:** Includes scripts for deploying agents on Windows and Linux hosts.

---

## Architecture

- **Backend:** Python Flask REST API
- **Frontend:** HTML, Jinja2 templates, Tailwind CSS, Chart.js
- **Metrics:** Prometheus, Node Exporter
- **Visualization:** Grafana (Docker)
- **Database:** SQLite (for device info and status)

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm (for frontend build)
- Docker (for Grafana and Prometheus)
- Git

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/M-o-j-o/NetMon.git
   cd NetMon
   ```

2. **Set up Python environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate # On Linux/Mac
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```sh
   npm install
   npx tailwindcss -i ./static/css/globals.css -o ./static/css/tailwind.css --watch
   ```

4. **Start Flask app:**
   ```sh
   python app.py
   ```

5. **Start Prometheus and Grafana (Docker):**
   ```sh
   docker-compose up -d
   ```

---

## Usage

- **Web Dashboard:**  
  Visit [http://localhost:5000](http://localhost:5000) to access the NetMon dashboard.
- **Add Devices:**  
  Use the "Add Device" form in the UI or POST to `/api/devices/add` via curl or Postman.
- **View Metrics:**  
  See real-time charts and Grafana dashboards for system performance.
- **Device Status:**  
  Devices are pinged and their status is updated automatically.

---

## Example: Add Device via API

```sh
curl -X POST http://localhost:5000/api/devices/add ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Linux VM\", \"ip_address\": \"192.168.56.101\", \"device_type\": \"server\", \"port\": 22, \"description\": \"Ubuntu VM\", \"tags\": [\"linux\",\"vm\"]}"
```

---

## Deployment

- **Windows Agent:**  
  Use `deploy_windows.bat` to deploy the monitoring agent on Windows hosts.
- **Linux Agent:**  
  Use the provided shell script or instructions for Linux hosts.

---

## Customization

- **Add custom metrics:**  
  Integrate with Prometheus exporters for more device stats.
- **Modify UI:**  
  Edit Jinja2 templates and Tailwind CSS for branding.
- **Extend API:**  
  Add new endpoints for device management or alerting.

---

## Troubleshooting

- **Styling Issues:**  
  Ensure Tailwind CSS is built and referenced correctly in `base.html`.
- **Database Errors:**  
  Delete `devices.db` if schema changes cause index errors.
- **Chart Bugs:**  
  Limit Chart.js data points and set fixed container heights.

---

## Contributing

Pull requests and issues are welcome!  
Please fork the repo and submit your changes via PR.

---

## License

MIT License

---

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)