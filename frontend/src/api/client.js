const BASE = ''

async function req(path, opts = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  })
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`)
  return res.json()
}

export const api = {
  getStats:     ()              => req('/stats'),
  getHeatmap:   ()              => req('/ips'),
  getTimeline:  ()              => req('/threats?limit=100'),
  getThreats:   (params = '')   => req(`/threats${params}`),
  getAlerts:    (unread = false)=> req(`/alerts${unread ? '?unread_only=true' : ''}`),
  ackAlert:     (id)            => req(`/alerts/${id}/acknowledge`, { method: 'PATCH' }),
  getLogs:      (params = '')   => req(`/logs${params}`),
  getIPProfile: (ip)            => req(`/ips/${ip}`),
  unblockIP:    (ip)            => req(`/ips/${ip}/unblock`, { method: 'POST' }),
  analyze:      (body)          => req('/analyze', { method: 'POST', body: JSON.stringify(body) }),
  uploadLogs:   (file, source)  => {
    const fd = new FormData()
    fd.append('file', file)
    return fetch(`/logs/upload?source=${source}`, { method: 'POST', body: fd }).then(r => r.json())
  },
}
