import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { RiskBadge, Spinner, EmptyState, PageHeader } from '../components/UI'
import { format } from 'date-fns'

const LEVELS = ['', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
const TYPES  = ['', 'bruteforce', 'burst', 'endpoint_hammering', 'enumeration', 'suspicious_ua', 'injection', 'none']

export default function Threats() {
  const [level, setLevel] = useState('')
  const [type, setType]   = useState('')

  const params = [level && `risk_level=${level}`, type && `attack_type=${type}`]
    .filter(Boolean).join('&')

  const { data, loading, refetch } = useFetch(
    () => api.getThreats(params ? `?${params}` : ''),
    [level, type]
  )

  return (
    <div className="space-y-4">
      <PageHeader title="Threats" subtitle="All detected threat events">
        <button onClick={refetch} className="text-xs px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg text-gray-600 shadow-sm">
          Refresh
        </button>
      </PageHeader>

      <div className="flex gap-3">
        <select value={level} onChange={e => setLevel(e.target.value)}
          className="bg-white border border-gray-200 text-sm text-gray-700 rounded-lg px-3 py-1.5 shadow-sm">
          {LEVELS.map(l => <option key={l} value={l}>{l || 'All Levels'}</option>)}
        </select>
        <select value={type} onChange={e => setType(e.target.value)}
          className="bg-white border border-gray-200 text-sm text-gray-700 rounded-lg px-3 py-1.5 shadow-sm">
          {TYPES.map(t => <option key={t} value={t}>{t || 'All Types'}</option>)}
        </select>
      </div>

      {loading ? <Spinner /> : (
        <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
          <div className="grid grid-cols-7 text-xs text-gray-500 uppercase tracking-wide px-4 py-2 border-b border-gray-100 bg-gray-50">
            <span>Time</span><span>IP</span><span>Attack</span>
            <span>Endpoint</span><span>Score</span><span>Level</span><span>AI Score</span>
          </div>
          <div className="divide-y divide-gray-50 max-h-[calc(100vh-260px)] overflow-y-auto">
            {!data?.length ? <EmptyState /> : data.map(t => (
              <div key={t.id} className="grid grid-cols-7 px-4 py-2.5 text-sm items-center hover:bg-gray-50">
                <span className="text-gray-400 text-xs">{format(new Date(t.detected_at), 'MM/dd HH:mm')}</span>
                <span className="font-mono text-xs text-gray-700">{t.ip}</span>
                <span className="text-xs capitalize text-gray-600">{t.attack_type}</span>
                <span className="text-gray-500 text-xs truncate">{t.endpoint}</span>
                <span className="font-bold text-gray-900">{t.risk_score}</span>
                <RiskBadge level={t.risk_level} />
                <span className="text-gray-400 text-xs">{(t.ai_score * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
