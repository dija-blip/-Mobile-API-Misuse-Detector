import clsx from 'clsx'

export default function Navbar({ connected }) {
  return (
    <header className="h-12 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0 shadow-sm">
      <span className="text-sm text-gray-500 font-medium">Mobile API Abuse Detector</span>
      <div className="flex items-center gap-2 text-xs">
        <span className={clsx('w-2 h-2 rounded-full', connected ? 'bg-green-500 animate-pulse' : 'bg-red-400')} />
        <span className={connected ? 'text-green-600 font-medium' : 'text-red-500'}>
          {connected ? 'Live' : 'Disconnected'}
        </span>
      </div>
    </header>
  )
}
