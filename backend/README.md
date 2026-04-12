# API de Detección y Clasificación de Microalgas

Servidor FastAPI que actúa como **proxy de inferencia** hacia modelos YOLO desplegados en **Ultralytics HUB / Cloud Run**. Procesa imágenes microscópicas y retorna detecciones con bounding boxes o clasificaciones por especie.

---

## Arquitectura general

```
Cliente (imagen JPG/PNG)
        │
        ▼
┌──────────────────────────────────────┐
│  FastAPI  (backend/)                 │
│                                      │
│  POST /detect           → classify() │  ──►  HUB_MODEL_URL  (clasificación)
│  POST /detect/annotated → predict()  │  ──►  HUB_DETECT_URL (detección YOLO)
│  GET  /health                        │
└──────────────────────────────────────┘
        │
        ▼
Ultralytics HUB / Cloud Run
  - Modelo clasificación: HUB_MODEL_URL
  - Modelo detección:     https://predict-69dadffce0a5df348caf-dproatj77a-uc.a.run.app
```

El servidor **no carga ningún modelo localmente** — toda la inferencia es remota vía HTTP.

---

## Clases del dataset VisAlgae 2023

| ID | Especie |
|----|---------|
| 0  | Platymonas |
| 1  | Chlorella |
| 2  | Dunaliella salina |
| 3  | Effrenium |
| 4  | Porphyridium |
| 5  | Haematococcus |

---

## Endpoints

### `GET /health`
Verifica que el servidor está activo y las variables de entorno del HUB están configuradas.

**Respuesta:**
```json
{
  "status": "ok",
  "model_url": "https://hub.ultralytics.com/models/<ID>"
}
```

---

### `POST /detect`
Recibe una imagen microscópica y devuelve la **clasificación** de la microalga (top-1).

Llama al modelo configurado en `HUB_MODEL_URL`.

**Query params:**
| Parámetro | Tipo  | Default | Rango      | Descripción |
|-----------|-------|---------|------------|-------------|
| `conf`    | float | 0.25    | 0.01–1.0   | Umbral de confianza |
| `iou`     | float | 0.45    | 0.01–1.0   | Umbral IoU para NMS |
| `imgsz`   | int   | 640     | 32–1920    | Resolución de inferencia |

**Form-data:** campo `file` con la imagen (JPEG / PNG / BMP / TIFF).

**Respuesta:**
```json
{
  "class_name": "Chlorella",
  "confidence": 0.9312
}
```

---

### `POST /detect/annotated`
Recibe una imagen microscópica y devuelve las **detecciones con bounding boxes** más la imagen anotada en base64.

Llama al modelo configurado en `HUB_DETECT_URL` (detección YOLO con cajas).

**Query params:** igual que `/detect`.

**Form-data:** campo `file` con la imagen.

**Respuesta:**
```json
{
  "total_detections": 3,
  "counts_by_class": {
    "Chlorella": 2,
    "Haematococcus": 1
  },
  "detections": [
    {
      "class_id": 1,
      "class_name": "Chlorella",
      "confidence": 0.9102,
      "bbox_xyxy": [0.12, 0.08, 0.45, 0.52],
      "bbox_px": [76, 51, 288, 332]
    }
  ],
  "annotated_image": "data:image/png;base64,iVBOR..."
}
```

El campo `bbox_xyxy` contiene coordenadas **normalizadas** (0–1); `bbox_px` contiene coordenadas en **píxeles absolutos**.

---

## Estructura de archivos

```
backend/
├── main.py          # Punto de entrada FastAPI, CORS, startup check
├── config.py        # Variables de entorno (HUB_API_KEY, HUB_MODEL_URL, HUB_DETECT_URL…)
├── model.py         # Cliente HTTP hacia Ultralytics HUB (_call_hub, classify, predict)
├── schemas.py       # Modelos Pydantic (BoundingBox, DetectionResponse, HealthResponse…)
├── routes/
│   └── detect.py    # Router FastAPI con los 3 endpoints
├── Dockerfile       # Imagen Docker python:3.11-slim con OpenCV headless
└── requirements.txt
```

---

## Variables de entorno

Copia `backend/.env.example` → `backend/.env` y rellena los valores:

| Variable        | Requerida | Descripción |
|-----------------|-----------|-------------|
| `HUB_API_KEY`   | ✅ Sí     | Clave de API de Ultralytics HUB (`https://hub.ultralytics.com/settings/api-keys`) |
| `HUB_MODEL_URL` | ✅ Sí     | URL del modelo de **clasificación** desplegado en HUB |
| `HUB_DETECT_URL`| ✅ Sí     | URL del modelo de **detección** (por defecto: Cloud Run del experimento exp-5) |
| `IMGSZ`         | No        | Resolución de inferencia por defecto (default: `640`) |
| `CONF_DEFAULT`  | No        | Umbral de confianza por defecto (default: `0.25`) |
| `IOU_DEFAULT`   | No        | Umbral IoU por defecto (default: `0.45`) |
| `HOST`          | No        | Host del servidor (default: `0.0.0.0`) |
| `PORT`          | No        | Puerto (default: `8000`) |
| `WORKERS`       | No        | Número de workers Uvicorn (default: `1`) |

---

## Modelo de detección (exp-5)

El modelo de detección activo fue entrenado con **YOLO26n** sobre el dataset **visalgae2023-v3**:

| Métrica   | Valor  |
|-----------|--------|
| mAP50     | 91.6%  |
| mAP50-95  | 70.6%  |
| Precision | 88.0%  |
| Recall    | 82.7%  |

- **Epochs:** 100  
- **Batch:** configurable  
- **GPU:** RTX PRO 6000  
- **Endpoint:** `https://predict-69dadffce0a5df348caf-dproatj77a-uc.a.run.app`

---

## Ejecución local

### Con uvicorn (desarrollo)
```bash
# Desde la raíz del repositorio
cp backend/.env.example backend/.env
# Editar backend/.env con las claves

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Con Docker Compose (producción local)
```bash
docker compose up --build
```

Documentación interactiva disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc:       `http://localhost:8000/redoc`

---

## Ejemplo de uso con curl

```bash
# Clasificación
curl -X POST http://localhost:8000/detect \
  -F "file=@imagen_microscopio.jpg"

# Detección con bounding boxes + imagen anotada
curl -X POST "http://localhost:8000/detect/annotated?conf=0.3" \
  -F "file=@imagen_microscopio.jpg"
```

---

## Diagrama de flujo de `model.py`

```
_call_hub(image, conf, iou, imgsz, url)
  │
  ├── cv2.imencode → JPEG bytes
  ├── httpx.Client.post(url, headers={"x-api-key": ...}, files={"file": ...})
  └── response.json()

classify()        → _call_hub(url=HUB_MODEL_URL)  → lista [{class_name, confidence}]
predict()         → _call_hub(url=HUB_DETECT_URL) → lista [{class_id, class_name, confidence, bbox_xyxy, bbox_px}]
predict_annotated() → predict() + _draw_boxes()   → (detecciones, imagen_BGR_anotada)
```


Servidor FastAPI que delega la inferencia YOLOv8 a Ultralytics HUB.
No requiere GPU ni carga de modelo localmente.

## Estructura

```
backend/
├── __init__.py
├── config.py          # Variables de entorno
├── model.py           # Cliente HTTP → Ultralytics HUB
├── schemas.py         # Modelos Pydantic de request/response
├── main.py            # App FastAPI + punto de entrada uvicorn
├── requirements.txt   # Dependencias
├── Dockerfile
├── .env               # Credenciales (no se versiona)
├── .env.example       # Plantilla de credenciales
└── routes/
    ├── __init__.py
    └── detect.py      # Endpoints de detección
```

## Configuración

Crea `backend/.env` con tus credenciales de Ultralytics HUB:

```env
HUB_API_KEY=tu_api_key
HUB_MODEL_URL=https://predict-xxxxx.a.run.app
```

Obtén la API key en: https://hub.ultralytics.com/settings/api-keys

## Ejecución con Docker (recomendado)

```bash
# Desde la raíz del repositorio
docker compose up --build
```

La API quedará disponible en `http://localhost:8000`.

## Ejecución local

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

| Método | Ruta                  | Descripción                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | `/health`             | Estado del servidor y configuración del HUB      |
| POST   | `/detect`             | Imagen → JSON con detecciones y conteo por clase |
| POST   | `/detect/annotated`   | Imagen → JSON + imagen anotada en base64 (PNG)   |
| GET    | `/docs`               | Documentación interactiva Swagger UI             |

## Ejemplo de uso

```bash
# Health check
curl http://localhost:8000/health

# Detección
curl -X POST "http://localhost:8000/detect?conf=0.25" \
     -F "file=@imagen_microscopio.jpg"

# Con imagen anotada
curl -X POST "http://localhost:8000/detect/annotated" \
     -F "file=@imagen_microscopio.jpg" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
with open('resultado.png', 'wb') as f:
    f.write(base64.b64decode(data['annotated_image'].split(',')[1]))
print('Conteo:', data['counts_by_class'])
"
```

## Variables de entorno

| Variable        | Requerida | Descripción                             |
|-----------------|-----------|-----------------------------------------|
| `HUB_API_KEY`   | Sí        | API key de Ultralytics HUB              |
| `HUB_MODEL_URL` | Sí        | URL del endpoint de inferencia del HUB  |
| `IMGSZ`         | No (640)  | Tamaño de inferencia                    |
| `CONF_DEFAULT`  | No (0.25) | Umbral de confianza                     |
| `IOU_DEFAULT`   | No (0.45) | Umbral IoU para NMS                     |
| `PORT`          | No (8000) | Puerto del servidor                     |
