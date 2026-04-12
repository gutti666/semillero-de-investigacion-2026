export default function DetectSummary({ total, classCounts }) {
  const classCount = Object.keys(classCounts ?? {}).length
  return (
    <div className="space-y-4">
      {/* Stat cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-bg-card border border-border rounded-xl p-4 text-center">
          <p className="text-teal text-4xl font-black leading-none">{total}</p>
          <p className="text-text-dim text-xs mt-1.5">Detecciones totales</p>
        </div>
        <div className="bg-bg-card border border-border rounded-xl p-4 text-center">
          <p className="text-teal text-4xl font-black leading-none">{classCount}</p>
          <p className="text-text-dim text-xs mt-1.5">Clases detectadas</p>
        </div>
      </div>

      {/* Class pills */}
      {classCount > 0 && (
        <div className="flex flex-wrap gap-2">
          {Object.entries(classCounts).map(([cls, cnt]) => (
            <span
              key={cls}
              className="text-xs font-bold px-3 py-1 rounded-full bg-bg-card2 border border-border text-white"
            >
              {cls}
              <span className="text-teal ml-1.5">{cnt}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
