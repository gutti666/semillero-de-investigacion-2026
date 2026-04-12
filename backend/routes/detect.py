"""
Router de detección de microalgas.
Endpoints:
  GET  /health                 — estado del servidor y modelo
  POST /detect                 — JSON con detecciones
  POST /detect/annotated       — JSON con detecciones + imagen anotada en base64
"""

import base64
import logging
from typing import Annotated

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse

from backend.config import ALLOWED_CONTENT_TYPES, CONF_DEFAULT, IOU_DEFAULT, IMGSZ, HUB_MODEL_URL
from backend.model import classify, predict_annotated
from backend.schemas import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()

_RESPONSES_DETECT = {
    415: {"description": "Tipo de imagen no soportado"},
    422: {"description": "Imagen no decodificable"},
}


# ── Utilidad interna ──────────────────────────────────────────────────────

def _decode_upload(raw: bytes) -> np.ndarray:
    """Convierte bytes de imagen subida a array BGR (OpenCV)."""
    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo decodificar la imagen. Verifica el formato.")
    return img


def _build_counts(detections: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for d in detections:
        counts[d["class_name"]] = counts.get(d["class_name"], 0) + 1
    return counts


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.get("/health", summary="Estado del servidor")
def health() -> HealthResponse:
    """Verifica que el servidor está activo y la configuración del HUB es válida."""
    from backend.config import HUB_API_KEY
    configured = bool(HUB_API_KEY and HUB_MODEL_URL)
    return HealthResponse(
        status="ok" if configured else "warning: HUB_API_KEY o HUB_MODEL_URL no definidos",
        model_url=HUB_MODEL_URL or "(no configurado)",
    )


@router.post(
    "/detect",
    summary="Clasificar microalga — respuesta JSON",
    responses=_RESPONSES_DETECT,
)
async def detect(
    request: Request,
    conf: Annotated[float, Query(ge=0.01, le=1.0, description="Umbral de confianza")] = CONF_DEFAULT,
    iou:  Annotated[float, Query(ge=0.01, le=1.0, description="Umbral IoU para NMS")]  = IOU_DEFAULT,
    imgsz: Annotated[int,  Query(ge=32,   le=1920, description="Tamaño de inferencia")] = IMGSZ,
) -> JSONResponse:
    """
    Recibe una imagen microscópica y devuelve la clasificación del alga.

    Respuesta:
    - `class_name`: nombre de la microalga clasificada
    - `confidence`: confianza del modelo (0-1)
    """
    form = await request.form()
    logger.info("=== /detect REQUEST DEBUG ===")
    logger.info("content-type header: %s", request.headers.get("content-type"))
    logger.info("form keys: %s", list(form.keys()))
    for k, v in form.multi_items():
        logger.info("  field key=%r  type=%s  preview=%r", k, type(v).__name__, str(v)[:80])

    file: UploadFile | None = next(
        (v for v in form.values() if hasattr(v, "filename") and hasattr(v, "read")), None
    )
    logger.info("UploadFile found=%s  filename=%s  content_type=%s",
                file is not None, getattr(file, 'filename', None), getattr(file, 'content_type', None))

    if file is None:
        raise HTTPException(status_code=422, detail="Se requiere un archivo en el form-data (campo 'file' o 'File').")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de archivo no soportado: '{file.content_type}'. "
                   f"Usa: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}",
        )

    raw = await file.read()
    try:
        img = _decode_upload(raw)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    results = classify(img, conf=conf, iou=iou, imgsz=imgsz)

    if not results:
        return JSONResponse({"class_name": None, "confidence": None})

    top = results[0]
    logger.info("classify | file=%s  class=%s  confidence=%s", file.filename, top["class_name"], top["confidence"])

    return JSONResponse({
        "class_name": top["class_name"],
        "confidence": top["confidence"],
    })


@router.post(
    "/detect/annotated",
    summary="Detectar microalgas — JSON + imagen anotada (base64)",
    responses=_RESPONSES_DETECT,
)
async def detect_annotated(
    request: Request,
    conf:  Annotated[float, Query(ge=0.01, le=1.0)] = CONF_DEFAULT,
    iou:   Annotated[float, Query(ge=0.01, le=1.0)] = IOU_DEFAULT,
    imgsz: Annotated[int,   Query(ge=32,   le=1920)] = IMGSZ,
) -> JSONResponse:
    """
    Igual que `/detect` pero incluye la imagen anotada con bounding boxes
    codificada en base64 PNG para visualización directa en el cliente.
    """
    form = await request.form()
    logger.info("=== /detect/annotated REQUEST DEBUG ===")
    logger.info("content-type header: %s", request.headers.get("content-type"))
    logger.info("form keys: %s", list(form.keys()))
    for k, v in form.multi_items():
        logger.info("  field key=%r  type=%s  preview=%r", k, type(v).__name__, str(v)[:80])

    file: UploadFile | None = next(
        (v for v in form.values() if hasattr(v, "filename") and hasattr(v, "read")), None
    )
    logger.info("UploadFile found=%s  filename=%s  content_type=%s",
                file is not None, getattr(file, 'filename', None), getattr(file, 'content_type', None))

    if file is None:
        raise HTTPException(status_code=422, detail="Se requiere un archivo en el form-data (campo 'file' o 'File').")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de archivo no soportado: '{file.content_type}'.",
        )

    raw = await file.read()
    try:
        img = _decode_upload(raw)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    detections, annotated_bgr = predict_annotated(img, conf=conf, iou=iou, imgsz=imgsz)
    counts = _build_counts(detections)

    _, buf = cv2.imencode(".png", annotated_bgr)
    img_b64 = base64.b64encode(buf).decode("utf-8")

    logger.info(
        "detect/annotated | file=%s  total=%d  counts=%s",
        file.filename, len(detections), counts,
    )

    return JSONResponse({
        "total_detections": len(detections),
        "counts_by_class" : counts,
        "detections"      : detections,
        "annotated_image" : f"data:image/png;base64,{img_b64}",
    })
