@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");
@import "tailwindcss";
@import "tw-animate-css";

:root {
  /* Colors inspired by Vercel's observability dashboard */
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --radius: 0.625rem;
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
  --success: rgb(34, 197, 94);
  --warning: rgb(245, 158, 11);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.637 0.237 25.331);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(0.269 0 0);
  --sidebar-ring: oklch(0.439 0 0);
}

@theme inline {
  /* optional: --font-sans, --font-serif, --font-mono if they are applied in the layout.tsx */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

@layer base {
  * {
    border-color: var(--border);
    outline-color: rgba(var(--ring), 0.5);
  }
  body {
    background-color: var(--background);
    color: var(--foreground);
  }
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Status indicators */
.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
}

.status-healthy {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--success);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-warning {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning);
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.status-critical {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--destructive);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-unknown {
  background-color: rgba(107, 114, 128, 0.1);
  color: rgb(107, 114, 128);
  border: 1px solid rgba(107, 114, 128, 0.2);
}

/* Cards */
.card {
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.card:hover {
  border-color: rgba(59, 130, 246, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--foreground);
}

.card-subtitle {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-top: 0.25rem;
}

/* Metrics */
.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--foreground);
  line-height: 1;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-top: 0.25rem;
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

.metric-change.positive {
  color: var(--success);
}

.metric-change.negative {
  color: var(--destructive);
}

/* Navigation */
.nav-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
}

.nav-tab {
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  color: var(--muted-foreground);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.nav-tab.active {
  color: var(--foreground);
  border-bottom-color: var(--primary);
}

.nav-tab:hover {
  color: var(--foreground);
}

.navbar {
  background-color: var(--card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: var(--muted-foreground);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--foreground);
  border-bottom-color: var(--primary);
}

/* Alerts */
.alert {
  padding: 1rem;
  border-radius: var(--radius);
  margin-bottom: 1rem;
  border-left: 4px solid;
}

.alert-critical {
  background-color: rgba(239, 68, 68, 0.1);
  border-left-color: var(--destructive);
  color: var(--destructive);
}

.alert-warning {
  background-color: rgba(245, 158, 11, 0.1);
  border-left-color: var(--warning);
  color: var(--warning);
}

.alert-info {
  background-color: rgba(59, 130, 246, 0.1);
  border-left-color: var(--primary);
  color: var(--primary);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--primary-foreground);
  border-color: var(--primary);
}

.btn-primary:hover {
  background-color: rgba(59, 130, 246, 0.9);
}

.btn-secondary {
  background-color: var(--secondary);
  color: var(--secondary-foreground);
  border-color: var(--border);
}

.btn-secondary:hover {
  background-color: var(--accent);
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.btn-destructive {
  background-color: var(--destructive);
  color: var(--destructive-foreground);
  border-color: var(--destructive);
}

.btn-destructive:hover {
  background-color: rgba(239, 68, 68, 0.9);
}

/* Grid layouts */
.grid {
  display: grid;
  gap: 1.5rem;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, 1fr);
}
.grid-cols-2 {
  grid-template-columns: repeat(2, 1fr);
}
.grid-cols-3 {
  grid-template-columns: repeat(3, 1fr);
}
.grid-cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Grafana iframe styling */
.grafana-panel {
  width: 100%;
  height: 400px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background-color: var(--card);
}

/* Loading states */
.loading {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid var(--muted);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive utilities */
.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-4 {
  gap: 1rem;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.text-sm {
  font-size: 0.875rem;
}

.text-xs {
  font-size: 0.75rem;
}

.font-medium {
  font-weight: 500;
}

.font-semibold {
  font-weight: 600;
}

.flex-wrap {
  flex-wrap: wrap;
}

.gap-1 {
  gap: 0.25rem;
}

.gap-2 {
  gap: 0.5rem;
}

.text-warning {
  color: rgb(245, 158, 11);
}

.text-destructive {
  color: var(--destructive);
}

.text-muted-foreground {
  color: var(--muted-foreground);
}

.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.capitalize {
  text-transform: capitalize;
}

/* Tables */
.table-container {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--card);
}

.table th,
.table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.table th {
  background-color: var(--muted);
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.table tbody tr:hover {
  background-color: var(--accent);
}

.table tbody tr:last-child td {
  border-bottom: none;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: calc(var(--radius) - 2px);
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-server {
  background-color: rgba(59, 130, 246, 0.1);
  color: rgb(59, 130, 246);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.badge-network {
  background-color: rgba(34, 197, 94, 0.1);
  color: rgb(34, 197, 94);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.badge-printer {
  background-color: rgba(168, 85, 247, 0.1);
  color: rgb(168, 85, 247);
  border: 1px solid rgba(168, 85, 247, 0.2);
}

.badge-storage {
  background-color: rgba(245, 158, 11, 0.1);
  color: rgb(245, 158, 11);
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.badge-other {
  background-color: rgba(107, 114, 128, 0.1);
  color: rgb(107, 114, 128);
  border: 1px solid rgba(107, 114, 128, 0.2);
}

/* Tags */
.tag {
  display: inline-block;
  padding: 0.125rem 0.375rem;
  background-color: var(--secondary);
  color: var(--secondary-foreground);
  border-radius: calc(var(--radius) - 4px);
  font-size: 0.75rem;
  font-weight: 500;
}

/* Forms */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--foreground);
}

.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background-color: var(--background);
  color: var(--foreground);
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--ring);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.input:invalid {
  border-color: var(--destructive);
}

/* Modals */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--foreground);
}

.modal-content form {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

/* Dark mode adjustments */
.dark .table th {
  background-color: var(--muted);
}

.dark .modal {
  background-color: rgba(0, 0, 0, 0.8);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .table-container {
    font-size: 0.875rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 0.5rem;
  }
}

let systemChart = null;

function renderSystemChart(metrics) {
    const ctx = document.getElementById('systemChart').getContext('2d');
    if (!systemChart) {
        systemChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [new Date().toLocaleTimeString()],
                datasets: [{
                    label: 'CPU Usage',
                    data: [metrics.cpu_usage],
                    borderColor: '#3b82f6',
                    fill: false
                }]
            },
            options: {
                animation: false,
                scales: {
                    x: { display: true },
                    y: { min: 0, max: 100 }
                }
            }
        });
    } else {
        // Update chart data
        systemChart.data.labels.push(new Date().toLocaleTimeString());
        systemChart.data.datasets[0].data.push(metrics.cpu_usage);

        // Limit data points to last 20
        if (systemChart.data.labels.length > 20) {
            systemChart.data.labels.shift();
            systemChart.data.datasets[0].data.shift();
        }

        systemChart.update();
    }
}

setInterval(() => {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(metrics => {
            renderSystemChart(metrics);
        });
}, 5000); // update every 5 seconds
