import { NavLink } from 'react-router-dom'
import { Shield, Activity, Bell, Clock, Map, Smartphone, FileText, Lightbulb, Upload, LayoutDashboard } from 'lucide-react'
import clsx from 'clsx'

const NAV = [
  { to: '/',             icon: LayoutDashboard, label: 'Overview' },
  { to: '/live',         icon: Activity,        label: 'Live Traffic' },
  { to: '/threats',      icon: Shield,          label: 'Threats' },
  { to: '/alerts',       icon: Bell,            label: 'Alerts' },
  { to: '/timeline',     icon: Clock,           label: 'Timeline' },
  { to: '/heatmap',      icon: Map,             label: 'Risk Heatmap' },
  { to: '/devices',      icon: Smartphone,      label: 'Devices' },
  { to: '/logs',         icon: FileText,        label: 'Logs' },
  { to: '/recommendations', icon: Lightbulb,   label: 'Recommendations' },
  { to: '/upload',       icon: Upload,          label: 'Import Logs' },
]

export default function Sidebar() {
  return (
    <aside className="w-56 shrink-0 bg-white border-r border-gray-200 flex flex-col h-screen sticky top-0 shadow-sm">
      <div className="px-5 py-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Shield size={20} className="text-blue-600" />
          <span className="font-bold text-sm text-gray-800 leading-tight">API Abuse<br/>Detector</span>
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end={to === '/'}
            className={({ isActive }) => clsx(
              'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
              isActive
                ? 'bg-blue-50 text-blue-700 font-medium'
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            )}>
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="px-4 py-3 border-t border-gray-200 text-xs text-gray-400">v4.0.0</div>
    </aside>
  )
}
