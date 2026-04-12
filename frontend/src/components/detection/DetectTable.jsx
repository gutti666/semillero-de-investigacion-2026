function formatBbox(bbox_px) {
  if (!bbox_px || bbox_px.every((v) => v === 0)) return '—'
  const [x1, y1, x2, y2] = bbox_px
  return `(${x1}, ${y1}) → (${x2}, ${y2})`
}

export default function DetectTable({ detections = [] }) {
  if (detections.length === 0) return null

  const hasBbox = detections.some((d) => d.bbox_px?.some((v) => v !== 0))

  return (
    <div className="overflow-x-auto rounded-xl border border-border mt-5">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-bg-card2 text-teal text-[0.72rem] uppercase tracking-widest">
            <th className="px-4 py-2.5 text-left border-b border-border">#</th>
            <th className="px-4 py-2.5 text-left border-b border-border">Clase</th>
            <th className="px-4 py-2.5 text-left border-b border-border">Confianza</th>
            {hasBbox && (
              <th className="px-4 py-2.5 text-left border-b border-border">BBox (px)</th>
            )}
          </tr>
        </thead>
        <tbody>
          {detections.map((d, i) => (
            <tr key={i} className={i % 2 === 0 ? 'bg-bg' : 'bg-[#0b1c10]'}>
              <td className="px-4 py-2 text-text-dim">{i + 1}</td>
              <td className="px-4 py-2 text-white font-medium">{d.class_name ?? '—'}</td>
              <td className="px-4 py-2">
                <span className="inline-block px-2.5 py-0.5 rounded-full bg-[#0d3020] border border-green-dim text-green text-[0.73rem] font-bold">
                  {((d.confidence ?? 0) * 100).toFixed(1)}%
                </span>
              </td>
              {hasBbox && (
                <td className="px-4 py-2 font-mono text-[0.73rem] text-text-dim">
                  {formatBbox(d.bbox_px)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
