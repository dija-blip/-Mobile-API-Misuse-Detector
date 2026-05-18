import { Activity, Shield, Bell, Ban } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { StatCard, Spinner, EmptyState, PageHeader } from '../components/UI'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'

const PIE_COLORS = ['#22c55e', '#f59e0b', '#f97316', '#ef4444', '#8b5cf6']

export default function Overview() {
  const { data: stats, loading } = useFetch(api.getStats)

  if (loading) return <Spinner />

  const rpm = stats?.requests_per_minute ?? []
  const attacks = stats?.top_attack_types ?? []

  return (
    <div className="space-y-6">
      <PageHeader title="Overview" subtitle="Platform-wide security summary" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Requests"   value={stats?.total_requests?.toLocaleString()} icon={Activity} color="text-blue-600" />
        <StatCard label="Unique IPs"       value={stats?.unique_ips?.toLocaleString()}     icon={Shield}   color="text-purple-600" />
        <StatCard label="Threats Detected" value={stats?.threats_detected?.toLocaleString()} icon={Bell}  color="text-orange-500" />
        <StatCard label="Blocked IPs"      value={stats?.blocked_ips?.toLocaleString()}    icon={Ban}      color="text-red-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Requests / Minute (last 60 min)</h2>
          {rpm.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={rpm}>
                <defs>
                  <linearGradient id="rpmGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="minute" tick={{ fontSize: 10, fill: '#9ca3af' }} tickFormatter={v => v?.slice(11, 16)} />
                <YAxis tick={{ fontSize: 10, fill: '#9ca3af' }} />
                <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8 }} />
                <Area type="monotone" dataKey="count" stroke="#3b82f6" fill="url(#rpmGrad)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top Attack Types</h2>
          {attacks.length === 0 ? <EmptyState /> : (
            <>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={attacks} dataKey="count" nameKey="type" cx="50%" cy="50%" outerRadius={65} strokeWidth={0}>
                    {attacks.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
              <ul className="space-y-1 mt-2">
                {attacks.map((a, i) => (
                  <li key={a.type} className="flex items-center justify-between text-xs">
                    <span className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full" style={{ background: PIE_COLORS[i % PIE_COLORS.length] }} />
                      <span className="text-gray-700 capitalize">{a.type}</span>
                    </span>
                    <span className="text-gray-400">{a.count}</span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm flex items-center gap-6">
        <div>
          <p className="text-gray-500 text-sm">Average Risk Score</p>
          <p className="text-4xl font-bold text-gray-900 mt-1">{stats?.avg_risk_score ?? 0}<span className="text-lg text-gray-400">/100</span></p>
        </div>
        <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full rounded-full bg-gradient-to-r from-green-400 via-yellow-400 to-red-500"
            style={{ width: `${stats?.avg_risk_score ?? 0}%` }} />
        </div>
      </div>
    </div>
  )
}
