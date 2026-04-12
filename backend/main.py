"""
Punto de entrada de la aplicación FastAPI.
Inicia el servidor: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import HOST, PORT, RELOAD, WORKERS
from backend.routes.detect import router as detect_router

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── FastAPI app ────────────────────────────────────────────────────────────
app = FastAPI(
    title="API de Detección de Microalgas",
    description=(
        "Servidor de inferencia YOLOv8 para detección y clasificación de tipos "
        "de microalgas en imágenes microscópicas de alta densidad.\n\n"
        "Dataset: [High-Throughput Algae Cell Detection](https://www.kaggle.com/datasets/marquis03/high-throughput-algae-cell-detection)"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────
# Ajusta origins según el entorno (restringir en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────
app.include_router(detect_router, tags=["Detección"])


# ── Arranque: validar configuración de HUB ────────────────────────────────
@app.on_event("startup")
async def _check_hub_config():
    """Verifica al arrancar que las variables de entorno del HUB están definidas."""
    from backend.config import HUB_API_KEY, HUB_MODEL_URL
    if not HUB_API_KEY or not HUB_MODEL_URL:
        logger.warning(
            "⚠  Variables de entorno no configuradas:\n"
            "%s%s"
            "Define ambas antes de hacer inferencia (ver backend/.env.example).",
            "  • HUB_API_KEY   — falta\n" if not HUB_API_KEY  else "",
            "  • HUB_MODEL_URL — falta\n" if not HUB_MODEL_URL else "",
        )
    else:
        logger.info("Configuración de Ultralytics HUB detectada correctamente.")


# ── Entrypoint ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        reload=RELOAD,
    )
