// Chart.js export for compatibility with dashboard.js imports
// This file provides Chart.js as a named export to satisfy import statements

// Re-export Chart from the global Chart.js library loaded via CDN
export const Chart =
  window.Chart ||
  (() => {
    console.warn("Chart.js not loaded. Make sure Chart.js is included via CDN in your HTML template.")
    return null
  })()

// Default export for convenience
export default Chart
