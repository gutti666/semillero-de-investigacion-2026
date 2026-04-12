"""
Schemas Pydantic para request/response de la API.
"""

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    class_id: int
    class_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox_xyxy: list[float] = Field(..., min_length=4, max_length=4,
                                   description="[x1, y1, x2, y2] normalizado 0-1")
    bbox_px: list[int] = Field(..., min_length=4, max_length=4,
                               description="[x1, y1, x2, y2] en píxeles")


class DetectionResponse(BaseModel):
    total_detections: int
    counts_by_class: dict[str, int]
    detections: list[BoundingBox]
    image_size: dict[str, int] = Field(description='{"width": px, "height": px}')


class AnnotatedDetectionResponse(BaseModel):
    total_detections: int
    counts_by_class: dict[str, int]
    detections: list[BoundingBox]
    annotated_image: str = Field(description="data:image/png;base64,<...>")


class HealthResponse(BaseModel):
    status: str
    model_url: str
