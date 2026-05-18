import { useWebSocket } from '../hooks/useWebSocket'
import { RiskBadge, PageHeader, EmptyState } from '../components/UI'
import { formatDistanceToNow } from 'date-fns'
import clsx from 'clsx'

export default function LiveTraffic() {
  const { events, connected } = useWebSocket(100)

  return (
    <div className="space-y-4">
      <PageHeader title="Live Traffic" subtitle="Real-time API request stream via WebSocket">
        <span className={clsx('text-xs px-3 py-1 rounded-full font-medium border',
          connected ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-600 border-red-200')}>
          {connected ? '● Live' : '○ Reconnecting...'}
        </span>
      </PageHeader>

      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <div className="grid grid-cols-6 text-xs text-gray-500 uppercase tracking-wide px-4 py-2 border-b border-gray-100 bg-gray-50">
          <span>Time</span><span>IP</span><span>Endpoint</span>
          <span>Attack</span><span>Score</span><span>Level</span>
        </div>
        <div className="divide-y divide-gray-50 max-h-[calc(100vh-220px)] overflow-y-auto">
          {events.length === 0
            ? <EmptyState message="Waiting for live events — send a request to /analyze" />
            : events.map((e, i) => (
              <div key={i} className={clsx(
                'grid grid-cols-6 px-4 py-2.5 text-sm items-center',
                e.risk_level === 'CRITICAL' ? 'bg-red-50' :
                e.risk_level === 'HIGH'     ? 'bg-orange-50' : 'hover:bg-gray-50'
              )}>
                <span className="text-gray-400 text-xs">
                  {e.timestamp ? formatDistanceToNow(new Date(e.timestamp), { addSuffix: true }) : 'just now'}
                </span>
                <span className="font-mono text-xs text-gray-700">{e.ip}</span>
                <span className="text-gray-500 text-xs truncate">{e.endpoint}</span>
                <span className="text-xs capitalize text-gray-600">{e.attack_type ?? '—'}</span>
                <span className="font-bold text-gray-900">{e.risk_score ?? 0}</span>
                <RiskBadge level={e.risk_level} />
              </div>
            ))
          }
        </div>
      </div>
    </div>
  )
}
