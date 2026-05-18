import { useEffect, useRef, useState, useCallback } from 'react'

export function useWebSocket(maxEvents = 50) {
  const [events, setEvents] = useState([])
  const [connected, setConnected] = useState(false)
  const wsRef = useRef(null)
  const retryRef = useRef(null)

  const connect = useCallback(() => {
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/live`)
    wsRef.current = ws

    ws.onopen = () => setConnected(true)
    ws.onclose = () => {
      setConnected(false)
      retryRef.current = setTimeout(connect, 3000)
    }
    ws.onerror = () => ws.close()
    ws.onmessage = (e) => {
      try {
        const parsed = JSON.parse(e.data)
        // Backend sends {type, data} — flatten to just data with type attached
        const event = parsed.data ? { ...parsed.data, _type: parsed.type } : parsed
        setEvents(prev => [event, ...prev].slice(0, maxEvents))
      } catch {}
    }
  }, [maxEvents])

  useEffect(() => {
    connect()
    return () => {
      clearTimeout(retryRef.current)
      wsRef.current?.close()
    }
  }, [connect])

  return { events, connected }
}
