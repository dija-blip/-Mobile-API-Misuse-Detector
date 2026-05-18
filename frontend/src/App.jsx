import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import { useWebSocket } from './hooks/useWebSocket'

import Overview        from './pages/Overview'
import LiveTraffic     from './pages/LiveTraffic'
import Threats         from './pages/Threats'
import Alerts          from './pages/Alerts'
import Timeline        from './pages/Timeline'
import Heatmap         from './pages/Heatmap'
import Devices         from './pages/Devices'
import Logs            from './pages/Logs'
import Recommendations from './pages/Recommendations'
import UploadLogs      from './pages/UploadLogs'

export default function App() {
  const { connected } = useWebSocket()

  return (
    <BrowserRouter>
      <div className="flex h-screen overflow-hidden">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Navbar connected={connected} />
          <main className="flex-1 overflow-y-auto p-6">
            <Routes>
              <Route path="/"                element={<Overview />} />
              <Route path="/live"            element={<LiveTraffic />} />
              <Route path="/threats"         element={<Threats />} />
              <Route path="/alerts"          element={<Alerts />} />
              <Route path="/timeline"        element={<Timeline />} />
              <Route path="/heatmap"         element={<Heatmap />} />
              <Route path="/devices"         element={<Devices />} />
              <Route path="/logs"            element={<Logs />} />
              <Route path="/recommendations" element={<Recommendations />} />
              <Route path="/upload"          element={<UploadLogs />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}
