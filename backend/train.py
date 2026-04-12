"""
Script de entrenamiento YOLOv8 para detección de microalgas.

Uso:
    python -m backend.train
    python -m backend.train --epochs 100 --imgsz 1280 --model yolov8s.pt
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

import kagglehub
from ultralytics import YOLO

from backend.config import (
    BASE_DIR,
    DATASET_DIR,
    DATASET_SLUG,
    DATASET_YAML,
    MODEL_BASE,
    RUNS_DIR,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def download_dataset() -> None:
    """Descarga el dataset desde Kaggle si no existe en la ruta estándar."""
    if DATASET_DIR.exists() and any(DATASET_DIR.iterdir()):
        logger.info("Dataset ya disponible en: %s", DATASET_DIR)
        return

    logger.info("Descargando dataset desde Kaggle: %s", DATASET_SLUG)
    try:
        downloaded = Path(kagglehub.dataset_download(DATASET_SLUG))
        logger.info("Descarga completada: %s", downloaded)

        DATASET_DIR.parent.mkdir(parents=True, exist_ok=True)
        if DATASET_DIR.exists():
            shutil.rmtree(DATASET_DIR)
        shutil.copytree(downloaded, DATASET_DIR)
        logger.info("Dataset copiado a ruta estándar: %s", DATASET_DIR)

    except Exception as exc:
        logger.error(
            "Fallo la descarga automática: %s\n"
            "Descarga manualmente el dataset y colócalo en:\n  %s",
            exc, DATASET_DIR,
        )
        sys.exit(1)


def _load_classes_from_yaml(dataset_path: Path) -> tuple[list[str], int]:
    """Extrae nombres de clases y nc del YAML original del dataset."""
    import yaml

    original_yaml = next(dataset_path.rglob("*.yaml"), None)
    if not original_yaml:
        logger.warning("No se encontró YAML original; clases serán inferidas.")
        return [], 0

    with open(original_yaml) as f:
        cfg = yaml.safe_load(f)

    classes = cfg.get("names", [])
    nc      = cfg.get("nc", len(classes))
    logger.info("Clases detectadas (%d): %s", nc, classes)
    return classes, nc


def _detect_splits(dataset_path: Path) -> dict[str, Path]:
    """Detecta las carpetas images/ de cada split (train/val/test)."""
    split_paths: dict[str, Path] = {}

    for lbl_dir in dataset_path.rglob("labels"):
        if not lbl_dir.is_dir():
            continue
        img_dir = lbl_dir.parent / "images"
        if not img_dir.exists():
            continue

        raw   = lbl_dir.parent.name.lower()
        split = "val" if raw in {"valid", "validation"} else raw
        n     = len(list(img_dir.glob("*.*")))

        already = split_paths.get(split)
        if already is None or n > len(list(already.glob("*.*"))):
            split_paths[split] = img_dir

    return split_paths


def _rel(base: Path, p: Path) -> str:
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)


def generate_yaml(dataset_path: Path) -> Path:
    """
    Genera algae_dataset.yaml detectando automáticamente los splits
    y las clases desde el YAML original del dataset.
    """
    import yaml

    classes, nc  = _load_classes_from_yaml(dataset_path)
    split_paths  = _detect_splits(dataset_path)

    yaml_content: dict = {
        "path" : str(dataset_path.resolve()),
        "train": _rel(dataset_path, split_paths["train"]) if "train" in split_paths else "images/train",
        "val"  : _rel(dataset_path, split_paths["val"])   if "val"   in split_paths else "images/val",
        "nc"   : nc or len(classes),
        "names": classes or [f"microalga_{i}" for i in range(nc or 1)],
    }
    if "test" in split_paths:
        yaml_content["test"] = _rel(dataset_path, split_paths["test"])

    DATASET_YAML.parent.mkdir(parents=True, exist_ok=True)
    with open(DATASET_YAML, "w") as f:
        yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

    logger.info("dataset.yaml generado: %s", DATASET_YAML)
    return DATASET_YAML


def train(
    epochs: int = 300,
    imgsz: int = 640,
    model_base: str = MODEL_BASE,
    run_name: str = "train_v1",
) -> Path:
    """
    Entrena YOLOv8 con fine-tuning ajustado para imágenes microscópicas de algas.

    Returns:
        Ruta al mejor modelo entrenado (best.pt).
    """
    # 1. Dataset
    download_dataset()

    dataset_path = next(
        (p for p in [
            DATASET_DIR / "versions" / "3",
            DATASET_DIR / "versions" / "2",
            DATASET_DIR / "versions" / "1",
            DATASET_DIR,
        ] if p.exists()),
        DATASET_DIR,
    )

    yaml_path = generate_yaml(dataset_path)

    # 2. Modelo base
    logger.info("Iniciando entrenamiento con: %s", model_base)
    model = YOLO(model_base)

    # 3. Entrenamiento con augmentation específica para microscopía
    model.train(
        data       = str(yaml_path),
        epochs     = epochs,
        imgsz      = imgsz,
        batch      = -1,          # auto-detección según VRAM
        optimizer  = "auto",
        amp        = True,        # Mixed Precision FP16/FP32
        pretrained = True,        # Transfer learning desde COCO
        patience   = 50,          # Early stopping
        cache      = True,
        # Augmentation para imágenes microscópicas
        flipud     = 0.5,         # sin orientación canónica en microscopía
        fliplr     = 0.5,
        hsv_h      = 0.02,        # variación de tono (coloración de algas)
        hsv_s      = 0.6,
        hsv_v      = 0.4,
        mosaic     = 1.0,
        copy_paste = 0.15,        # compensa clases poco representadas
        mixup      = 0.05,
        project    = str(RUNS_DIR),
        name       = run_name,
        save       = True,
        save_period= 50,
    )

    best = RUNS_DIR / run_name / "weights" / "best.pt"
    if best.exists():
        logger.info("Entrenamiento completado. Mejor modelo: %s", best)
    else:
        logger.warning("No se encontró best.pt en la ruta esperada: %s", best)

    return best


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Entrenar YOLOv8 para detección de microalgas"
    )
    parser.add_argument("--epochs",  type=int,  default=300,          help="Número de épocas")
    parser.add_argument("--imgsz",   type=int,  default=640,          help="Tamaño de imagen")
    parser.add_argument("--model",   type=str,  default=MODEL_BASE,   help="Modelo base (ej: yolov8s.pt)")
    parser.add_argument("--name",    type=str,  default="train_v1",   help="Nombre del experimento")
    args = parser.parse_args()

    train(
        epochs     = args.epochs,
        imgsz      = args.imgsz,
        model_base = args.model,
        run_name   = args.name,
    )


if __name__ == "__main__":
    main()
