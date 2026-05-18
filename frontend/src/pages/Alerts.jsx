import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { RiskBadge, Spinner, EmptyState, PageHeader } from '../components/UI'
import { format } from 'date-fns'
import { CheckCircle } from 'lucide-react'

export default function Alerts() {
  const [unreadOnly, setUnreadOnly] = useState(false)
  const { data, loading, refetch } = useFetch(
    () => api.getAlerts(unreadOnly), [unreadOnly]
  )

  const ack = async (id) => {
    await api.ackAlert(id)
    refetch()
  }

  return (
    <div className="space-y-4">
      <PageHeader title="Alerts" subtitle="Security alerts requiring attention">
        <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
          <input type="checkbox" checked={unreadOnly} onChange={e => setUnreadOnly(e.target.checked)}
            className="accent-blue-600" />
          Unread only
        </label>
      </PageHeader>

      {loading ? <Spinner /> : (
        <div className="space-y-3">
          {!data?.length ? <EmptyState message="No alerts found" /> : data.map(a => (
            <div key={a.id} className={`bg-white border rounded-xl p-4 shadow-sm ${a.acknowledged ? 'border-gray-200 opacity-60' : 'border-orange-200'}`}>
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <RiskBadge level={a.risk_level} />
                    <span className="text-xs text-gray-400">{format(new Date(a.created_at), 'MMM dd, HH:mm:ss')}</span>
                  </div>
                  <p className="text-sm text-gray-900 font-medium">{a.message}</p>
                  <p className="text-xs text-gray-500 mt-1 font-mono">{a.ip} → {a.endpoint}</p>
                  {a.recommendation && (
                    <details className="mt-2">
                      <summary className="text-xs text-blue-600 cursor-pointer">View recommendations</summary>
                      <pre className="text-xs text-gray-600 mt-2 whitespace-pre-wrap bg-gray-50 rounded-lg p-3 border border-gray-100">{a.recommendation}</pre>
                    </details>
                  )}
                </div>
                {!a.acknowledged && (
                  <button onClick={() => ack(a.id)}
                    className="shrink-0 flex items-center gap-1 text-xs text-green-600 hover:text-green-700 px-2 py-1 bg-green-50 border border-green-200 rounded-lg">
                    <CheckCircle size={14} /> Ack
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
