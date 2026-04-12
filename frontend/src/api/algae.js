import axios from 'axios'

// Se puede sobreescribir en tiempo de ejecución desde el input de la UI
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE ?? 'http://localhost:8000',
  timeout: 60_000,
})

/**
 * Actualiza la baseURL del cliente dinámicamente desde la UI
 * @param {string} url
 */
export function setApiBase(url) {
  apiClient.defaults.baseURL = url.replace(/\/$/, '')
}

/**
 * GET /health
 */
export async function fetchHealth(base) {
  const client = base
    ? axios.create({ baseURL: base.replace(/\/$/, ''), timeout: 5000 })
    : apiClient
  const { data } = await client.get('/health')
  return data
}

/**
 * POST /detect  → { class_name, confidence }
 * @param {File}   file
 * @param {number} conf
 * @param {number} iou
 * @param {number} imgsz
 */
export async function classifyAlga(file, conf = 0.25, iou = 0.45, imgsz = 640) {
  const fd = new FormData()
  fd.append('file', file)
  const { data } = await apiClient.post(
    `/detect?conf=${conf}&iou=${iou}&imgsz=${imgsz}`,
    fd,
    { headers: { 'Content-Type': 'multipart/form-data' } },
  )
  return data
}

/**
 * POST /detect/annotated  → { total_detections, counts_by_class, detections[], annotated_image }
 * @param {File}   file
 * @param {number} conf
 * @param {number} iou
 * @param {number} imgsz
 */
export async function detectAlgas(file, conf = 0.25, iou = 0.45, imgsz = 640) {
  const fd = new FormData()
  fd.append('file', file)
  const { data } = await apiClient.post(
    `/detect/annotated?conf=${conf}&iou=${iou}&imgsz=${imgsz}`,
    fd,
    { headers: { 'Content-Type': 'multipart/form-data' } },
  )
  return data
}
