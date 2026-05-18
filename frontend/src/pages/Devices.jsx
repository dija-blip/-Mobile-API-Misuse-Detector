import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Spinner, EmptyState, PageHeader } from '../components/UI'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts'
import { useMemo } from 'react'

const COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#22c55e', '#06b6d4', '#f97316', '#ec4899']

export default function Devices() {
  const { data: ips, loading } = useFetch(api.getHeatmap)

  const { byCountry, byRiskLevel, topIPs } = useMemo(() => {
    if (!ips?.length) return { byCountry: [], byRiskLevel: [], topIPs: [] }

    const cm = {}, rm = {}
    ips.forEach(p => {
      const c = p.country || 'Unknown'
      cm[c] = (cm[c] || 0) + 1
      rm[p.risk_level] = (rm[p.risk_level] || 0) + 1
    })

    const toArr = obj => Object.entries(obj)
      .map(([k, v]) => ({ name: k, count: v }))
      .sort((a, b) => b.count - a.count)

    return {
      byCountry: toArr(cm).slice(0, 8),
      byRiskLevel: toArr(rm),
      topIPs: [...ips].sort((a, b) => b.total_requests - a.total_requests).slice(0, 10)
        .map(p => ({ name: p.ip, count: p.total_requests })),
    }
  }, [ips])

  if (loading) return <Spinner />

  return (
    <div className="space-y-6">
      <PageHeader title="Device Analytics" subtitle="IP profiles, countries, and risk distribution" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top IPs by Requests</h2>
          {topIPs.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={topIPs} layout="vertical">
                <XAxis type="number" tick={{ fontSize: 10, fill: '#9ca3af' }} />
                <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 9, fill: '#6b7280' }} />
                <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8 }} />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {topIPs.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Risk Level Distribution</h2>
          {byRiskLevel.length === 0 ? <EmptyState /> : (
            <>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={byRiskLevel} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={65} strokeWidth={0}>
                    {byRiskLevel.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
              <ul className="space-y-1 mt-2">
                {byRiskLevel.map((r, i) => (
                  <li key={r.name} className="flex items-center justify-between text-xs">
                    <span className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full" style={{ background: COLORS[i % COLORS.length] }} />
                      <span className="text-gray-700">{r.name}</span>
                    </span>
                    <span className="text-gray-400">{r.count}</span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm lg:col-span-2">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">By Country</h2>
          {byCountry.length === 0 ? <EmptyState /> : (
            <ResponsiveContainer width="100%" height={160}>
              <BarChart data={byCountry}>
                <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#9ca3af' }} />
                <YAxis tick={{ fontSize: 10, fill: '#9ca3af' }} />
                <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8 }} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {byCountry.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  )
}
