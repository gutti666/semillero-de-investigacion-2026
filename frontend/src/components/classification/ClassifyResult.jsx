export default function ClassifyResult({ data }) {
  if (!data) return null

  const noDetection = !data.class_name

  const pct = noDetection ? 0 : Math.round(data.confidence * 1000) / 10

  return (
    <div className="mt-5 bg-bg-card border border-border rounded-2xl p-6">
      <p className="text-[0.72rem] font-bold text-text-dim uppercase tracking-widest mb-4">
        Resultado de Clasificación
      </p>

      {noDetection ? (
        <p className="text-text-dim italic text-sm">El modelo no encontró ningún alga con la confianza mínima establecida.</p>
      ) : (
        <>
          <p className="text-teal text-4xl font-black tracking-tight">{data.class_name}</p>

          <div className="mt-5">
            <div className="flex justify-between text-xs text-text-dim mb-1.5">
              <span>Confianza del modelo</span>
              <span className="text-green font-bold">{pct.toFixed(1)}%</span>
            </div>
            <div className="h-2 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-teal to-green shadow-[0_0_8px_#00e5b0] transition-all duration-700"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        </>
      )}
    </div>
  )
}
