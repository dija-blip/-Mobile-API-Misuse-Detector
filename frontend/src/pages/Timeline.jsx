import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Spinner, EmptyState, PageHeader, RiskBadge } from '../components/UI'
import { format } from 'date-fns'
import clsx from 'clsx'

const DOT_COLOR = {
  CRITICAL: 'bg-red-500',
  HIGH:     'bg-orange-400',
  MEDIUM:   'bg-yellow-400',
  LOW:      'bg-green-500',
}

export default function Timeline() {
  const { data, loading } = useFetch(api.getThreats)

  return (
    <div className="space-y-4">
      <PageHeader title="Attack Timeline" subtitle="Chronological view of all threat events" />
      {loading ? <Spinner /> : (
        <div className="relative pl-6 space-y-0">
          <div className="absolute left-2.5 top-0 bottom-0 w-px bg-gray-200" />
          {!data?.length ? <EmptyState message="No threats detected yet" /> : data.map((e, i) => (
            <div key={i} className="relative flex gap-4 pb-4">
              <span className={clsx('absolute -left-4 mt-1.5 w-3 h-3 rounded-full border-2 border-white shadow',
                DOT_COLOR[e.risk_level] ?? 'bg-gray-300')} />
              <div className="bg-white border border-gray-200 rounded-xl px-4 py-3 flex-1 hover:border-gray-300 shadow-sm transition-colors">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="text-xs text-gray-400">{format(new Date(e.detected_at), 'MMM dd, HH:mm:ss')}</span>
                  <RiskBadge level={e.risk_level} />
                </div>
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs text-gray-700">{e.ip}</span>
                  <span className="text-gray-300">·</span>
                  <span className="text-xs capitalize text-gray-500">{e.attack_type}</span>
                  <span className="text-gray-300">·</span>
                  <span className="text-xs font-bold text-gray-900">{e.risk_score}/100</span>
                  <span className="text-gray-300">·</span>
                  <span className="text-xs text-gray-500 truncate">{e.endpoint}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
