import clsx from 'clsx'

const LEVEL_STYLES = {
  LOW:      'bg-green-100 text-green-700 border border-green-200',
  MEDIUM:   'bg-yellow-100 text-yellow-700 border border-yellow-200',
  HIGH:     'bg-orange-100 text-orange-700 border border-orange-200',
  CRITICAL: 'bg-red-100 text-red-700 border border-red-200',
  none:     'bg-gray-100 text-gray-500 border border-gray-200',
}

export function RiskBadge({ level }) {
  return (
    <span className={clsx('px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wide',
      LEVEL_STYLES[level?.toUpperCase()] ?? LEVEL_STYLES.none)}>
      {level ?? 'N/A'}
    </span>
  )
}

export function StatCard({ label, value, icon: Icon, color = 'text-blue-600', sub }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 flex items-start gap-4 shadow-sm">
      {Icon && (
        <div className={clsx('p-2 rounded-lg bg-gray-50', color)}>
          <Icon size={20} />
        </div>
      )}
      <div>
        <p className="text-gray-500 text-sm">{label}</p>
        <p className="text-2xl font-bold text-gray-900 mt-0.5">{value ?? '—'}</p>
        {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
      </div>
    </div>
  )
}

export function Spinner() {
  return (
    <div className="flex items-center justify-center h-32">
      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )
}

export function EmptyState({ message = 'No data available' }) {
  return (
    <div className="flex flex-col items-center justify-center h-32 text-gray-400 text-sm gap-2">
      <span className="text-2xl">📭</span>
      {message}
    </div>
  )
}

export function PageHeader({ title, subtitle, children }) {
  return (
    <div className="flex items-start justify-between mb-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="text-gray-500 text-sm mt-1">{subtitle}</p>}
      </div>
      {children}
    </div>
  )
}
