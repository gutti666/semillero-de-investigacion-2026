import { useApi } from '../../context/ApiContext'

const dotClass = {
  online:  'bg-green shadow-[0_0_6px_#28f07c]',
  offline: 'bg-danger shadow-[0_0_6px_#ff5f5f]',
  loading: 'bg-warn animate-pulse',
}

export default function ApiBar() {
  const { apiBase, updateBase, status, checkHealth } = useApi()

  function handleBlur(e) {
    const val = e.target.value.trim()
    if (val) {
      updateBase(val)
      checkHealth(val)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') e.target.blur()
  }

  return (
    <div className="flex items-center gap-3 bg-bg-card border border-border rounded-xl px-4 py-2.5 mb-7">
      <span className="text-[0.72rem] font-bold text-teal uppercase tracking-widest whitespace-nowrap">
        API
      </span>
      <input
        className="flex-1 bg-transparent border-none outline-none text-white font-mono text-sm"
        defaultValue={apiBase}
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        spellCheck={false}
        aria-label="URL base del backend"
      />
      <div
        className={`w-2.5 h-2.5 rounded-full flex-shrink-0 transition-all ${dotClass[status]}`}
        title={status === 'online' ? 'Servidor en línea' : status === 'offline' ? 'Sin conexión' : 'Comprobando…'}
      />
    </div>
  )
}
