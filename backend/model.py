"""
Cliente HTTP para la API de inferencia de Ultralytics HUB.
Mantiene la misma interfaz que el módulo local para no modificar los routes.

Requiere las variables de entorno:
  HUB_API_KEY   — clave de API (https://hub.ultralytics.com/settings/api-keys)
  HUB_MODEL_URL — URL del modelo, e.g. https://hub.ultralytics.com/models/<ID>
"""

import logging

import cv2
import httpx
import numpy as np

from backend.config import HUB_API_KEY, HUB_MODEL_URL, HUB_DETECT_URL, CONF_DEFAULT, IOU_DEFAULT, IMGSZ

logger = logging.getLogger(__name__)



def _check_config(url: str | None = None) -> None:
    """Valida que la clave de API y la URL del modelo estén definidas."""
    if not HUB_API_KEY:
        raise RuntimeError(
            "Variable de entorno HUB_API_KEY no definida. "
            "Obtén tu clave en: https://hub.ultralytics.com/settings/api-keys"
        )
    if not url:
        raise RuntimeError(
            "URL del modelo no configurada. "
            "Ejemplo: https://hub.ultralytics.com/models/<MODEL_ID>"
        )


def _call_hub(image: np.ndarray, conf: float, iou: float, imgsz: int, url: str | None = None) -> dict:
    """Llama a un endpoint de Ultralytics HUB y retorna el JSON de respuesta."""
    target_url = url or HUB_MODEL_URL
    _check_config(target_url)

    ok, buf = cv2.imencode(".jpg", image)
    if not ok:
        raise ValueError("No se pudo codificar la imagen para enviarla a la API.")

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            target_url,
            headers={"x-api-key": HUB_API_KEY},
            data={"imgsz": imgsz, "conf": conf, "iou": iou},
            files={"file": ("image.jpg", buf.tobytes(), "image/jpeg")},
        )

    if response.status_code != 200:
        logger.error("HUB API error %s: %s", response.status_code, response.text)
        raise RuntimeError(
            f"Error de Ultralytics HUB ({response.status_code}): {response.text}"
        )

    logger.debug("HUB raw response: %s", response.text[:500])
    return response.json()


def classify(
    image: np.ndarray,
    conf: float = CONF_DEFAULT,
    iou: float = IOU_DEFAULT,
    imgsz: int = IMGSZ,
) -> list[dict]:
    """
    Envía la imagen al modelo de clasificación en Ultralytics HUB.

    Returns:
        Lista ordenada por confianza descendente. Cada elemento:
        - class_name: nombre de la clase
        - confidence: confianza entre 0 y 1 (4 decimales)
    """
    data = _call_hub(image, conf, iou, imgsz)
    raw_results = data.get("images", [{}])[0].get("results", [])

    results = [
        {
            "class_name": r.get("name", f"class_{r.get('class', i)}"),
            "confidence": round(float(r.get("confidence", 0.0)), 4),
        }
        for i, r in enumerate(raw_results)
    ]

    return sorted(results, key=lambda x: x["confidence"], reverse=True)


def predict(
    image: np.ndarray,
    conf: float = CONF_DEFAULT,
    iou: float = IOU_DEFAULT,
    imgsz: int = IMGSZ,
) -> list[dict]:
    """
    Envía la imagen al modelo de detección en Ultralytics HUB y retorna las
    detecciones con bounding boxes (modo detect).
    """
    data = _call_hub(image, conf, iou, imgsz, url=HUB_DETECT_URL)
    raw_results = data.get("images", [{}])[0].get("results", [])

    h, w = image.shape[:2]
    detections = []
    for r in raw_results:
        box = r.get("box", {})
        x1 = float(box.get("x1", 0))
        y1 = float(box.get("y1", 0))
        x2 = float(box.get("x2", 0))
        y2 = float(box.get("y2", 0))
        cls_id = int(r.get("class", 0))
        detections.append({
            "class_id"  : cls_id,
            "class_name": r.get("name", f"class_{cls_id}"),
            "confidence": round(float(r.get("confidence", 0.0)), 4),
            "bbox_xyxy" : [round(x1/w, 4), round(y1/h, 4), round(x2/w, 4), round(y2/h, 4)],
            "bbox_px"   : [int(x1), int(y1), int(x2), int(y2)],
        })
    return detections


def predict_annotated(
    image: np.ndarray,
    conf: float = CONF_DEFAULT,
    iou: float = IOU_DEFAULT,
    imgsz: int = IMGSZ,
) -> tuple[list[dict], np.ndarray]:
    """
    Igual que predict() pero también retorna la imagen BGR anotada con bboxes.

    Returns:
        (detecciones, imagen_anotada_bgr)
    """
    detections = predict(image, conf=conf, iou=iou, imgsz=imgsz)
    annotated = _draw_boxes(image.copy(), detections)
    return detections, annotated


def _draw_boxes(image: np.ndarray, detections: list[dict]) -> np.ndarray:
    """Dibuja bounding boxes y etiquetas directamente sobre la imagen."""
    for d in detections:
        x1, y1, x2, y2 = d["bbox_px"]
        label = f"{d['class_name']} {d['confidence']:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image, label, (x1, max(y1 - 5, 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA,
        )
    return image
