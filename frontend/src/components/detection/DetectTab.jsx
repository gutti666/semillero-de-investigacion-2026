import { useState } from 'react'
import DropZone from '../shared/DropZone'
import RangeSlider from '../shared/RangeSlider'
import Spinner from '../shared/Spinner'
import ErrorBox from '../shared/ErrorBox'
import DetectSummary from './DetectSummary'
import DetectImage from './DetectImage'
import DetectTable from './DetectTable'
import { useDetect } from '../../hooks/useDetect'

export default function DetectTab() {
  const [file, setFile]   = useState(null)
  const [conf, setConf]   = useState(0.25)
  const [iou,  setIou]    = useState(0.45)
  const [imgsz, setImgsz] = useState(640)

  const { mutate, data, isPending, error, reset } = useDetect()

  function handleFile(f) {
    reset()
    setFile(f)
  }

  function handleSubmit() {
    if (!file) return
    mutate({ file, conf, iou, imgsz })
  }

  const errMsg = error
    ? (error.response?.data?.detail ?? error.message ?? 'Error desconocido')
    : null

  return (
    <section className="space-y-0">
      <DropZone onFile={handleFile} icon="🔭" disabled={isPending} />

      {/* Controls */}
      <div className="flex flex-wrap items-end gap-5 mt-5">
        <RangeSlider id="conf-det" label="Confianza" value={conf} onChange={setConf} />
        <RangeSlider id="iou-det"  label="IoU"       value={iou}  onChange={setIou} />
        <RangeSlider id="imgsz-det" label="Img size" value={imgsz} onChange={setImgsz} min={32} max={1280} step={32} />

        <button
          onClick={handleSubmit}
          disabled={!file || isPending}
          className="
            ml-auto bg-gradient-to-r from-teal to-green text-[#072010]
            font-extrabold rounded-xl px-6 py-2.5 text-sm tracking-wide
            glow-btn transition-all duration-150
            hover:opacity-90 hover:-translate-y-0.5
            disabled:opacity-40 disabled:cursor-not-allowed disabled:translate-y-0
          "
        >
          {isPending ? 'Detectando…' : 'Detectar Algas'}
        </button>
      </div>

      <Spinner visible={isPending} />
      <ErrorBox message={errMsg} />

      {data && (
        <div className="mt-5 space-y-5">
          <DetectSummary
            total={data.total_detections ?? 0}
            classCounts={data.counts_by_class ?? {}}
          />
          <DetectImage src={data.annotated_image} />
          <DetectTable detections={data.detections ?? []} />
        </div>
      )}
    </section>
  )
}
