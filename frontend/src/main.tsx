import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// 1. Get the element first
const rootElement = document.getElementById('root')

// 2. Safety check: Only render if the element exists
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  )
} else {
  console.error("FATAL ERROR: Could not find root element. Is index.html missing <div id='root'></div>?")
}