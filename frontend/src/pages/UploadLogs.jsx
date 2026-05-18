import { useState, useRef } from 'react'
import { api } from '../api/client'
import { PageHeader } from '../components/UI'
import { Upload, CheckCircle, XCircle } from 'lucide-react'
import clsx from 'clsx'

export default function UploadLogs() {
  const [source, setSource] = useState('auto')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [drag, setDrag] = useState(false)
  const inputRef = useRef()

  const handleFile = async (file) => {
    if (!file) return
    setLoading(true)
    setResult(null)
    try {
      const res = await api.uploadLogs(file, source)
      setResult({ ok: true, ...res })
    } catch (e) {
      setResult({ ok: false, message: e.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 max-w-xl">
      <PageHeader title="Import Logs" subtitle="Upload Nginx, Express, or Spring Boot log files" />

      <div>
        <label className="text-xs text-gray-500 mb-1 block font-medium">Log Format</label>
        <select value={source} onChange={e => setSource(e.target.value)}
          className="bg-white border border-gray-200 text-sm text-gray-700 rounded-lg px-3 py-2 w-full shadow-sm">
          <option value="auto">Auto-detect</option>
          <option value="nginx">Nginx</option>
          <option value="express">Express.js (Winston JSON)</option>
          <option value="springboot">Spring Boot</option>
        </select>
      </div>

      <div
        onDragOver={e => { e.preventDefault(); setDrag(true) }}
        onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]) }}
        onClick={() => inputRef.current?.click()}
        className={clsx(
          'border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors',
          drag ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300 bg-white'
        )}>
        <Upload size={32} className="mx-auto text-gray-400 mb-3" />
        <p className="text-sm text-gray-500">Drop a log file here or <span className="text-blue-600">click to browse</span></p>
        <p className="text-xs text-gray-400 mt-1">.log, .txt files supported</p>
        <input ref={inputRef} type="file" accept=".log,.txt" className="hidden"
          onChange={e => handleFile(e.target.files[0])} />
      </div>

      {loading && (
        <div className="flex items-center gap-3 text-sm text-gray-500">
          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          Parsing and ingesting logs...
        </div>
      )}

      {result && (
        <div className={clsx('rounded-xl p-4 border', result.ok ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200')}>
          <div className="flex items-center gap-2 mb-2">
            {result.ok ? <CheckCircle size={16} className="text-green-600" /> : <XCircle size={16} className="text-red-500" />}
            <span className="text-sm font-medium text-gray-900">{result.ok ? 'Import successful' : 'Import failed'}</span>
          </div>
          {result.ok ? (
            <ul className="text-xs text-gray-600 space-y-1">
              <li>✓ Parsed: <span className="font-medium">{result.parsed}</span></li>
              <li>✗ Failed lines: <span className="font-medium">{result.failed}</span></li>
              <li>⚠ Threats detected: <span className="font-medium">{result.threats_detected}</span></li>
            </ul>
          ) : (
            <p className="text-xs text-red-600">{result.message}</p>
          )}
        </div>
      )}
    </div>
  )
}
