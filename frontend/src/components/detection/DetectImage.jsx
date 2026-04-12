export default function DetectImage({ src }) {
  if (!src) return null
  return (
    <div className="rounded-xl overflow-hidden border border-border bg-black">
      <img src={src} alt="Imagen anotada con bounding boxes" className="w-full h-auto block" />
      <p className="text-text-dim text-[0.72rem] text-center py-2 bg-bg-card border-t border-border">
        Imagen anotada con bounding boxes — generada por el servidor
      </p>
    </div>
  )
}
