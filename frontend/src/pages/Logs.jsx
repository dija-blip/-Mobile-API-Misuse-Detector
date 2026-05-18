import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { api } from '../api/client'
import { Spinner, EmptyState, PageHeader } from '../components/UI'
import { format } from 'date-fns'

const STATUS_COLOR = s =>
  s >= 500 ? 'text-red-600' : s >= 400 ? 'text-orange-500' : s >= 300 ? 'text-yellow-600' : 'text-green-600'

export default function Logs() {
  const [ip, setIp] = useState('')
  const [offset, setOffset] = useState(0)
  const LIMIT = 100

  const { data, loading, refetch } = useFetch(
    () => api.getLogs(`?limit=${LIMIT}&offset=${offset}${ip ? `&ip=${ip}` : ''}`),
    [offset, ip]
  )

  return (
    <div className="space-y-4">
      <PageHeader title="Log Browser" subtitle="Raw ingested API log entries">
        <button onClick={refetch} className="text-xs px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-lg text-gray-600 shadow-sm">
          Refresh
        </button>
      </PageHeader>

      <div className="flex gap-3">
        <input value={ip} onChange={e => { setIp(e.target.value); setOffset(0) }}
          placeholder="Filter by IP..."
          className="bg-white border border-gray-200 text-sm text-gray-700 rounded-lg px-3 py-1.5 w-48 shadow-sm" />
      </div>

      {loading ? <Spinner /> : (
        <>
          <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
            <div className="grid grid-cols-7 text-xs text-gray-500 uppercase tracking-wide px-4 py-2 border-b border-gray-100 bg-gray-50">
              <span>Time</span><span>IP</span><span>Method</span>
              <span>Endpoint</span><span>Status</span><span>RT (ms)</span><span>Source</span>
            </div>
            <div className="divide-y divide-gray-50 max-h-[calc(100vh-280px)] overflow-y-auto">
              {!data?.length ? <EmptyState /> : data.map(l => (
                <div key={l.id} className="grid grid-cols-7 px-4 py-2 text-xs items-center hover:bg-gray-50">
                  <span className="text-gray-400">{format(new Date(l.timestamp), 'MM/dd HH:mm:ss')}</span>
                  <span className="font-mono text-gray-700">{l.ip}</span>
                  <span className="text-blue-600 font-medium">{l.method}</span>
                  <span className="text-gray-500 truncate">{l.endpoint}</span>
                  <span className={STATUS_COLOR(l.status_code)}>{l.status_code}</span>
                  <span className="text-gray-500">{l.response_time_ms}</span>
                  <span className="text-gray-400 capitalize">{l.source}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="flex gap-2 justify-end">
            <button disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - LIMIT))}
              className="text-xs px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 disabled:opacity-40 rounded-lg text-gray-600 shadow-sm">
              ← Prev
            </button>
            <button disabled={!data || data.length < LIMIT} onClick={() => setOffset(offset + LIMIT)}
              className="text-xs px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 disabled:opacity-40 rounded-lg text-gray-600 shadow-sm">
              Next →
            </button>
          </div>
        </>
      )}
    </div>
  )
}
