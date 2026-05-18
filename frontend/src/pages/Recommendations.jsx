import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Spinner, EmptyState, PageHeader, RiskBadge } from '../components/UI'
import { useMemo } from 'react'
import { Lightbulb } from 'lucide-react'

export default function Recommendations() {
  const { data: alerts, loading } = useFetch(() => api.getAlerts())

  const grouped = useMemo(() => {
    if (!alerts) return {}
    const map = {}
    alerts.forEach(a => {
      if (!map[a.attack_type]) map[a.attack_type] = { recommendation: a.recommendation, count: 0, max_score: 0, risk_level: a.risk_level }
      map[a.attack_type].count++
      if (a.risk_score > map[a.attack_type].max_score) {
        map[a.attack_type].max_score = a.risk_score
        map[a.attack_type].risk_level = a.risk_level
      }
    })
    return map
  }, [alerts])

  if (loading) return <Spinner />
  const entries = Object.entries(grouped)

  return (
    <div className="space-y-4">
      <PageHeader title="Recommendations" subtitle="Automated defensive recommendations based on detected threats" />
      {entries.length === 0 ? <EmptyState message="No recommendations yet — analyze some traffic first" /> : (
        <div className="space-y-4">
          {entries.map(([type, info]) => (
            <div key={type} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <Lightbulb size={16} className="text-yellow-600" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 capitalize">{type.replace(/_/g, ' ')}</h3>
                    <p className="text-xs text-gray-400">{info.count} alert{info.count > 1 ? 's' : ''} · Max score: {info.max_score}</p>
                  </div>
                </div>
                <RiskBadge level={info.risk_level} />
              </div>
              <pre className="text-xs text-gray-600 whitespace-pre-wrap leading-relaxed bg-gray-50 rounded-lg p-3 border border-gray-100">
                {info.recommendation}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
