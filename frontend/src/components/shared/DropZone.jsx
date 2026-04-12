import { useDropzone } from 'react-dropzone'
import { useState } from 'react'

const MAX_SIZE = 10 * 1024 * 1024 // 10 MB

export default function DropZone({ onFile, icon = '🧫', disabled = false }) {
  const [preview, setPreview] = useState(null)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.webp'] },
    maxSize: MAX_SIZE,
    maxFiles: 1,
    disabled,
    onDropAccepted: (files) => {
      const file = files[0]
      setPreview({ url: URL.createObjectURL(file), name: file.name, size: file.size })
      onFile(file)
    },
  })

  return (
    <div className="space-y-3">
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer
          transition-all duration-200 select-none
          ${isDragActive
            ? 'border-teal bg-[#0d2818]'
            : 'border-border bg-bg-card hover:border-teal hover:bg-[#0d2818]'}
          ${disabled ? 'opacity-40 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        <span className="text-5xl block mb-3">{icon}</span>
        <p className="text-white font-semibold text-sm">
          {isDragActive ? 'Suelta la imagen aquí…' : 'Arrastra o selecciona una imagen microscópica'}
        </p>
        <p className="text-text-dim text-xs mt-1">JPG · PNG · WEBP — máx. 10 MB</p>
      </div>

      {preview && (
        <div className="flex items-center gap-3 bg-bg-card2 border border-border rounded-xl px-4 py-2.5">
          <img
            src={preview.url}
            alt="preview"
            className="w-14 h-14 object-cover rounded-lg border border-border flex-shrink-0"
          />
          <div>
            <p className="text-white text-sm font-semibold truncate max-w-xs">{preview.name}</p>
            <p className="text-text-dim text-xs mt-0.5">{(preview.size / 1024).toFixed(1)} KB</p>
          </div>
        </div>
      )}
    </div>
  )
}
