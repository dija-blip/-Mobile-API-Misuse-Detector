import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Spinner, EmptyState, PageHeader, RiskBadge } from '../components/UI'
import clsx from 'clsx'

function scoreColor(score) {
  if (score >= 75) return 'bg-red-100 border-red-300 text-red-800'
  if (score >= 50) return 'bg-orange-100 border-orange-300 text-orange-800'
  if (score >= 25) return 'bg-yellow-100 border-yellow-300 text-yellow-800'
  return 'bg-green-100 border-green-300 text-green-800'
}

export default function Heatmap() {
  const { data, loading } = useFetch(api.getHeatmap)

  return (
    <div className="space-y-4">
      <PageHeader title="Risk Heatmap" subtitle="IP risk scores — color indicates threat level" />
      {loading ? <Spinner /> : !data?.length ? <EmptyState message="No IP profiles yet — analyze some traffic first" /> : (
        <div className="grid grid-cols-5 sm:grid-cols-8 lg:grid-cols-10 gap-2">
          {data.map((d, i) => (
            <div key={i}
              title={`${d.ip}\nScore: ${d.risk_score}\nRequests: ${d.total_requests}`}
              className={clsx('border rounded-lg p-2 cursor-default transition-transform hover:scale-105 shadow-sm', scoreColor(d.risk_score))}>
              <p className="text-xs font-mono truncate">{d.ip}</p>
              <p className="text-lg font-bold">{d.risk_score}</p>
              <p className="text-xs opacity-70">{d.total_requests} req</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
