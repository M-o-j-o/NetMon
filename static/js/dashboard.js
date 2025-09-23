import { Chart } from "@/components/ui/chart"
// Dashboard JavaScript functionality for Network Monitoring
// Uses Chart.js loaded via CDN in HTML template

class NetworkDashboard {
  constructor() {
    this.refreshInterval = 30000 // 30 seconds
    this.charts = {}
    this.init()
  }

  init() {
    this.setupEventListeners()
    this.loadInitialData()
    this.startAutoRefresh()
    this.initializeCharts()
  }

  setupEventListeners() {
    // Time range selector
    document.querySelectorAll(".time-range-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".time-range-btn").forEach((b) => b.classList.remove("active"))
        e.target.classList.add("active")
        this.updateTimeRange(e.target.dataset.range)
      })
    })

    // Tab navigation
    document.querySelectorAll(".nav-tab").forEach((tab) => {
      tab.addEventListener("click", (e) => {
        e.preventDefault()
        document.querySelectorAll(".nav-tab").forEach((t) => t.classList.remove("active"))
        document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"))

        e.target.classList.add("active")
        const targetId = e.target.getAttribute("href").substring(1)
        document.getElementById(targetId).classList.add("active")
      })
    })

    // Refresh button
    document.getElementById("refreshBtn")?.addEventListener("click", () => {
      this.loadInitialData()
    })

    // Alert dismiss buttons
    document.querySelectorAll(".alert-dismiss").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.target.closest(".alert").style.display = "none"
      })
    })
  }

  async loadInitialData() {
    try {
      // Load system metrics
      const metricsResponse = await fetch("/api/metrics")
      const metrics = await metricsResponse.json()
      this.updateMetrics(metrics)

      // Load device status
      const devicesResponse = await fetch("/api/devices")
      const devices = await devicesResponse.json()
      this.updateDeviceStatus(devices)

      // Load alerts
      const alertsResponse = await fetch("/api/alerts")
      const alerts = await alertsResponse.json()
      this.updateAlerts(alerts)
    } catch (error) {
      console.error("Error loading dashboard data:", error)
    }
  }

  updateMetrics(metrics) {
    // Update metric cards
    document.getElementById("cpu-usage").textContent = `${metrics.cpu}%`
    document.getElementById("memory-usage").textContent = `${metrics.memory}%`
    document.getElementById("network-io").textContent = `${metrics.network} MB/s`
    document.getElementById("disk-usage").textContent = `${metrics.disk}%`

    // Update charts
    this.updateCharts(metrics)
  }

  updateDeviceStatus(devices) {
    const deviceList = document.getElementById("device-list")
    if (!deviceList) return

    deviceList.innerHTML = devices
      .map(
        (device) => `
      <div class="device-item">
        <div class="device-info">
          <div class="device-name">${device.name}</div>
          <div class="device-ip">${device.ip}</div>
        </div>
        <div class="device-status">
          <span class="status-indicator ${device.status}"></span>
          <span class="response-time">${device.responseTime}ms</span>
        </div>
      </div>
    `,
      )
      .join("")
  }

  updateAlerts(alerts) {
    const alertContainer = document.getElementById("alert-container")
    if (!alertContainer) return

    alertContainer.innerHTML = alerts
      .map(
        (alert) => `
      <div class="alert alert-${alert.severity}">
        <div class="alert-content">
          <div class="alert-title">${alert.title}</div>
          <div class="alert-message">${alert.message}</div>
          <div class="alert-time">${new Date(alert.timestamp).toLocaleString()}</div>
        </div>
        <button class="alert-dismiss">&times;</button>
      </div>
    `,
      )
      .join("")

    // Re-attach dismiss listeners
    document.querySelectorAll(".alert-dismiss").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.target.closest(".alert").style.display = "none"
      })
    })
  }

  initializeCharts() {
    // CPU Usage Chart
    const cpuCtx = document.getElementById("cpuChart")?.getContext("2d")
    if (cpuCtx) {
      this.charts.cpu = new Chart(cpuCtx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "CPU Usage %",
              data: [],
              borderColor: "#3b82f6",
              backgroundColor: "rgba(59, 130, 246, 0.1)",
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: "#e5e7eb" },
            },
          },
          scales: {
            x: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
            },
            y: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
              min: 0,
              max: 100,
            },
          },
        },
      })
    }

    // Memory Usage Chart
    const memoryCtx = document.getElementById("memoryChart")?.getContext("2d")
    if (memoryCtx) {
      this.charts.memory = new Chart(memoryCtx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "Memory Usage %",
              data: [],
              borderColor: "#10b981",
              backgroundColor: "rgba(16, 185, 129, 0.1)",
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: "#e5e7eb" },
            },
          },
          scales: {
            x: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
            },
            y: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
              min: 0,
              max: 100,
            },
          },
        },
      })
    }

    // Network I/O Chart
    const networkCtx = document.getElementById("networkChart")?.getContext("2d")
    if (networkCtx) {
      this.charts.network = new Chart(networkCtx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "Network I/O MB/s",
              data: [],
              borderColor: "#f59e0b",
              backgroundColor: "rgba(245, 158, 11, 0.1)",
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: "#e5e7eb" },
            },
          },
          scales: {
            x: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
            },
            y: {
              ticks: { color: "#9ca3af" },
              grid: { color: "rgba(156, 163, 175, 0.1)" },
              min: 0,
            },
          },
        },
      })
    }
  }

  updateCharts(metrics) {
    const now = new Date().toLocaleTimeString()

    Object.keys(this.charts).forEach((chartKey) => {
      const chart = this.charts[chartKey]
      const value = metrics[chartKey]

      if (chart && value !== undefined) {
        chart.data.labels.push(now)
        chart.data.datasets[0].data.push(value)

        // Keep only last 20 data points
        if (chart.data.labels.length > 20) {
          chart.data.labels.shift()
          chart.data.datasets[0].data.shift()
        }

        chart.update("none")
      }
    })
  }

  updateTimeRange(range) {
    // Update Grafana iframes with new time range
    const timeRanges = {
      "1h": "from=now-1h&to=now",
      "6h": "from=now-6h&to=now",
      "12h": "from=now-12h&to=now",
      "24h": "from=now-24h&to=now",
      "7d": "from=now-7d&to=now",
    }

    const timeParam = timeRanges[range]
    document.querySelectorAll(".grafana-panel").forEach((iframe) => {
      const currentSrc = iframe.src
      const baseUrl = currentSrc.split("?")[0]
      const urlParams = new URLSearchParams(currentSrc.split("?")[1])

      // Update time parameters
      const newParams = timeParam.split("&")
      newParams.forEach((param) => {
        const [key, value] = param.split("=")
        urlParams.set(key, value)
      })

      iframe.src = `${baseUrl}?${urlParams.toString()}`
    })
  }

  startAutoRefresh() {
    setInterval(() => {
      this.loadInitialData()
    }, this.refreshInterval)
  }
}

// Initialize dashboard when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new NetworkDashboard()
})
