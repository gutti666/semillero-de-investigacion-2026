export default function RangeSlider({ id, label, min = 0.01, max = 1, step = 0.01, value, onChange }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center justify-between">
        <label htmlFor={id} className="text-[0.72rem] font-bold text-teal uppercase tracking-widest">
          {label}
        </label>
        <span className="text-[0.72rem] text-text-dim font-mono">{Number(value).toFixed(2)}</span>
      </div>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="
          w-32 h-1 rounded-full appearance-none cursor-pointer
          bg-border
          [&::-webkit-slider-thumb]:appearance-none
          [&::-webkit-slider-thumb]:w-3.5
          [&::-webkit-slider-thumb]:h-3.5
          [&::-webkit-slider-thumb]:rounded-full
          [&::-webkit-slider-thumb]:bg-teal
          [&::-webkit-slider-thumb]:shadow-[0_0_6px_#00e5b0]
        "
      />
    </div>
  )
}
