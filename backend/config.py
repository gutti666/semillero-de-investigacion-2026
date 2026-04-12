"""
Configuración central del backend.
Los valores se leen desde variables de entorno con fallback a defaults seguros.
"""

import os
from pathlib import Path

# ── Cargar .env si existe ──────────────────────────────────────────────────
_env_file = Path(__file__).resolve().parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

# ── Ultralytics HUB API ───────────────────────────────────────────────────
# Obtén tu API key en: https://hub.ultralytics.com/settings/api-keys
HUB_API_KEY   = os.getenv("HUB_API_KEY", "")
HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", "")   # modelo de clasificación
# Modelo de detección (bounding boxes) desplegado en Ultralytics HUB / Cloud Run
HUB_DETECT_URL = os.getenv(
    "HUB_DETECT_URL",
    "",
)

# ── Parámetros de inferencia ───────────────────────────────────────────────
IMGSZ        = int(os.getenv("IMGSZ", "640"))
CONF_DEFAULT = float(os.getenv("CONF_DEFAULT", "0.25"))
IOU_DEFAULT  = float(os.getenv("IOU_DEFAULT", "0.45"))

# ── Servidor ───────────────────────────────────────────────────────────────
HOST    = os.getenv("HOST", "0.0.0.0")
PORT    = int(os.getenv("PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", "1"))
RELOAD  = os.getenv("RELOAD", "false").lower() == "true"

# ── Tipos de imagen permitidos ─────────────────────────────────────────────
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/tiff",
}
