export default function Header() {
  return (
    <header className="text-center pt-12 pb-10">
      {/* Logo ring */}
      <div className="inline-flex items-center justify-center w-20 h-20 rounded-full border-2 border-teal glow-teal mb-5 bg-[radial-gradient(circle,#0f3320,#0c1f13)]">
        <svg viewBox="0 0 24 24" fill="none" stroke="#00e5b0" strokeWidth="1.6"
          strokeLinecap="round" strokeLinejoin="round" className="w-10 h-10">
          <path d="M6 18H4a2 2 0 0 1-2-2v-1h20v1a2 2 0 0 1-2 2h-2"/>
          <path d="M12 2v7"/><path d="M8 2h8"/><path d="M20 15H4"/>
          <circle cx="12" cy="11" r="3"/><path d="M12 14v4"/>
        </svg>
      </div>

      <h1 className="text-gradient text-5xl md:text-6xl font-black tracking-tight leading-none">
        AlgaeVision
      </h1>
      <p className="mt-3 text-text-dim text-sm md:text-base max-w-md mx-auto leading-relaxed">
        Detección Automática de Células de Microalgas mediante Aprendizaje Profundo — YOLOv8
      </p>

      <div className="flex gap-2 justify-center flex-wrap mt-4">
        {['YOLOv8', '6 clases', 'Deep Learning', 'Uniagustiniana'].map((b) => (
          <span
            key={b}
            className="text-[0.68rem] font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-border bg-bg-card text-teal"
          >
            {b}
          </span>
        ))}
      </div>
    </header>
  )
}
