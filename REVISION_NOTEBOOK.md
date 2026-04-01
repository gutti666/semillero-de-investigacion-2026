# Revisión del Notebook: `inicialización_datos_nuevodataset.ipynb`

## Semillero de Investigación 2026

---

## 1. Resumen General

El notebook realiza un análisis exploratorio de datos (EDA) del dataset **High-Throughput Algae Cell Detection** en formato YOLO. Incluye:

- Descarga/carga del dataset desde Kaggle
- Importación y configuración de librerías
- Exploración de la estructura del dataset
- Carga de configuración YOLO (`data.yaml`)
- Construcción de un DataFrame de anotaciones
- Estadísticas descriptivas y detección de datos faltantes
- Visualizaciones: distribución de clases, dimensiones de bounding boxes, distribución espacial de centros, anotaciones por imagen, matriz de correlación, imágenes de muestra con bounding boxes

---

## 2. Aspectos Positivos / Bien Implementados ✅

| # | Aspecto | Detalle |
|---|---------|---------|
| 1 | **Descarga idempotente del dataset** | La celda 2 verifica si el dataset ya existe antes de descargarlo, evitando descargas innecesarias. |
| 2 | **Búsqueda flexible de rutas** | La celda 3 prueba múltiples rutas candidatas para localizar el dataset, lo que aporta portabilidad entre máquinas. |
| 3 | **Manejo robusto de splits** | La celda 17 busca carpetas `labels` recursivamente y las empareja con carpetas `images` hermanas, detectando splits automáticamente. |
| 4 | **Normalización de nombres de splits** | Convierte `valid`/`validation` a `val` para homogeneizar nombres. |
| 5 | **Protección contra división por cero** | En el cálculo de `aspect_ratio` se valida que `h > 0` antes de dividir (`w / h if h > 0 else np.nan`). |
| 6 | **Manejo de errores en parseo de anotaciones** | El bloque `try/except` al leer archivos `.txt` captura errores sin interrumpir la ejecución. |
| 7 | **Validación de datos faltantes** | La celda 20 inspecciona y reporta nulos con porcentajes claros. |
| 8 | **Visualizaciones informativas** | Las gráficas son claras, bien tituladas y con etiquetas descriptivas. Incluyen medias como referencia. |
| 9 | **Muestreo estratificado** | La visualización de imágenes (celda 33) toma muestras por split para una representación equilibrada. |
| 10 | **Conversión correcta de bbox YOLO a píxeles** | La fórmula `x1 = (x_c - w/2) * img_w` es la correcta para YOLO → esquina superior izquierda. |

---

## 3. Problemas de Lógica y Errores Detectados 🔴

### 3.1. Celda 16 — Código Python en celda Markdown (Error crítico)

**Problema:** La celda 16 tiene `cell_type: "markdown"` pero contiene código Python ejecutable (búsqueda de carpetas labels, lógica de splits) mezclado con una tabla Markdown parcial. Este código **nunca se ejecuta**.

**Contenido problemático:**
```python
# Buscar cualquier carpeta 'labels' con archivos .txt ...
label_dirs = [d for d in dataset_path.rglob('labels') if d.is_dir()]
...
```
seguido de una tabla Markdown incompleta con descripciones de columnas.

**Impacto:** El código no se ejecuta pero confunde al lector. Además la tabla de descripción de columnas queda mal formada (le falta el encabezado de la tabla Markdown).

**Corrección sugerida:** Separar en dos celdas: (1) una celda Markdown con el encabezado de sección `## 7. Construcción del DataFrame de Anotaciones` y la tabla de columnas bien formateada, y (2) verificar que el código ya está incluido en la celda 17 (que sí se ejecuta).

---

### 3.2. Sección 7 ausente en la numeración

**Problema:** Las secciones saltan de **6. Carga de Configuración y Clases** directamente a **8. Análisis Visual Preliminar de Datos**. Falta la **Sección 7** que debería cubrir la construcción del DataFrame de anotaciones (celdas 17-20).

**Corrección sugerida:** Agregar una celda Markdown `## 7. Construcción del DataFrame de Anotaciones` antes de la celda 17, y mover la descripción de columnas (actualmente perdida en la celda 16 markdown) a esta nueva sección.

---

### 3.3. Celda 27 — Inconsistencia en orientación del eje Y del heatmap

**Problema:** En el gráfico de dispersión (axes[0]) se invierte el eje Y con `axes[0].invert_yaxis()` para alinearse con coordenadas de imagen (Y crece hacia abajo). Sin embargo, en el mapa de calor (axes[1]) se usa `origin='upper'` con `extent=[0, 1, 0, 1]`, lo cual muestra el eje Y de 0 (arriba) a 1 (abajo). Si bien ambos intentan representar la misma orientación, el `extent` con `[0, 1, 0, 1]` combinado con `origin='upper'` puede generar una inversión visual inesperada del eje Y: las etiquetas del eje mostrarán 0→1 de abajo hacia arriba, pero los datos se pintan de arriba hacia abajo.

**Corrección sugerida:** Usar `origin='lower'` con `extent=[0, 1, 0, 1]` y luego `axes[1].invert_yaxis()` para que sea visualmente consistente con el scatter plot. O bien usar `origin='upper'` con `extent=[0, 1, 1, 0]` para que el eje Y refleje correctamente que 0 está arriba.

---

### 3.4. Celda 7 — `except` genérico sin tipo de excepción

**Problema:**
```python
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('seaborn-darkgrid')
```
Usar `except:` sin especificar el tipo de excepción es mala práctica: captura cualquier error incluyendo `KeyboardInterrupt`, `SystemExit`, etc.

**Corrección sugerida:**
```python
except (OSError, ValueError):
    plt.style.use('seaborn-darkgrid')
```

---

### 3.5. Dataset config muestra `val` apuntando a train

**Observación:** El `data.yaml` del dataset define:
```yaml
train: ../train/images
val: ../train/images   # ← apunta a las mismas imágenes que train
test: ../test
```
El notebook no detecta ni alerta sobre esta anomalía. El split `val` no existe como carpeta independiente en el dataset, y las imágenes de validación son las mismas que las de entrenamiento. Esto es un **problema del dataset** (no del notebook), pero el notebook debería identificarlo.

**Corrección sugerida:** Agregar una celda de validación que compare las rutas del YAML y alerte si `train` y `val` apuntan al mismo directorio.

---

## 4. Aspectos a Mejorar ⚠️

### 4.1. Supresión global de warnings

**Celda 5:**
```python
warnings.filterwarnings('ignore')
```
Ocultar todos los warnings puede enmascarar problemas reales (deprecaciones, errores numéricos, etc.).

**Sugerencia:** Solo suprimir warnings específicos y conocidos, o activarlos durante el desarrollo y suprimirlos solo en la versión final.

---

### 4.2. Re-importación redundante de `Path` y otros módulos

`Path` de `pathlib` se importa en las celdas 2, 3, 5 y se vuelve a importar. `glob` se importa como módulo en la celda 5 pero nunca se usa (se usa `pathlib.Path.rglob()` en su lugar).

**Sugerencia:** Centralizar las importaciones en la celda 5 y eliminar importaciones duplicadas o no utilizadas.

---

### 4.3. Variable global `path` (string) compartida entre celdas

La celda 3 define `path = str(dataset_root.resolve())` como string, y la celda 13 la convierte de nuevo a `Path(path)`. Es más limpio mantener siempre un objeto `Path`.

**Sugerencia:** Usar una sola variable `dataset_path` de tipo `Path` desde la celda 3 y reutilizarla directamente.

---

### 4.4. Sin validación de rango de coordenadas YOLO

Las coordenadas YOLO deben estar normalizadas entre 0 y 1. El notebook no valida que `x_center`, `y_center`, `width`, `height` estén en el rango `[0, 1]`. Si hay anotaciones corruptas con valores fuera de rango, se incorporarían silenciosamente al DataFrame.

**Sugerencia:** Agregar una celda de validación:
```python
out_of_range = df[(df[['x_center','y_center','width','height']] < 0).any(axis=1) |
                  (df[['x_center','y_center','width','height']] > 1).any(axis=1)]
if len(out_of_range) > 0:
    print(f"⚠️ {len(out_of_range)} anotaciones con valores fuera del rango [0, 1]")
```

---

### 4.5. No se reportan imágenes sin anotaciones

El notebook cuenta imágenes y anotaciones por split, pero no identifica cuántas imágenes **no tienen archivo de etiqueta** correspondiente (posibles negativos o errores del dataset).

**Sugerencia:** Comparar la lista de archivos en `images/` con la de `labels/` y reportar diferencias.

---

### 4.6. El cálculo de `area` usa valores normalizados

El `area = width * height` se calcula con valores normalizados (0-1), lo que produce áreas muy pequeñas (media ≈ 0.0018). Esto es técnicamente correcto pero poco intuitivo. No se proporciona el área en píxeles reales.

**Sugerencia:** Considerar agregar una columna `area_px` calculada a partir de las dimensiones reales de las imágenes para análisis más interpretable (requiere leer al menos una imagen para obtener resolución).

---

### 4.7. Falta análisis de balance entre splits

El notebook muestra 701 imágenes train y 300 imágenes test, pero no analiza si la distribución de clases es proporcional entre splits (posible sesgo de muestreo).

**Sugerencia:** Agregar un análisis de proporciones de clase por split y verificar si están balanceadas.

---

### 4.8. No se verifica la existencia de un split de validación

Según la exploración, solo se encuentran splits `train` y `test`. No hay split de validación, lo cual es inusual para entrenamiento de modelos. El notebook no alerta sobre esto.

**Sugerencia:** Agregar un check que advierta si falta el split `val`/`valid` y recomiende crearlo mediante subdivisión del train.

---

### 4.9. Celda 33 — `plt.cm.get_cmap` deprecado

```python
cmap = plt.cm.get_cmap('tab10', max(n_classes, 10))
```
`get_cmap` está deprecado en versiones recientes de Matplotlib (≥3.9). Debería usarse `matplotlib.colormaps['tab10']`.

**Sugerencia:**
```python
cmap = plt.colormaps['tab10'].resampled(max(n_classes, 10))
```

---

### 4.10. Ausencia de resumen/conclusiones al final del notebook

El notebook termina abruptamente después de la visualización de imágenes sin una sección de conclusiones, hallazgos principales o próximos pasos.

**Sugerencia:** Agregar una celda Markdown final con:
- Resumen de hallazgos clave (número de clases, desbalance, distribución espacial)
- Problemas detectados en el dataset
- Próximos pasos recomendados (entrenamiento, aumento de datos, etc.)

---

## 5. Tabla Resumen de Prioridades

| Prioridad | Problema | Celda | Tipo |
|-----------|---------|-------|------|
| 🔴 Alta | Código Python en celda Markdown (no se ejecuta) | 16 | Error de estructura |
| 🔴 Alta | Sección 7 ausente en numeración | 16-17 | Error de estructura |
| 🟡 Media | Inconsistencia eje Y en heatmap vs scatter | 27 | Error de lógica visual |
| 🟡 Media | `except` genérico sin tipo | 7 | Mala práctica |
| 🟡 Media | No valida rango [0,1] de coordenadas YOLO | 17 | Omisión de validación |
| 🟡 Media | No detecta val==train en data.yaml | 15 | Omisión de validación |
| 🟢 Baja | Supresión global de warnings | 5 | Mala práctica |
| 🟢 Baja | Importaciones redundantes | 2,3,5 | Limpieza de código |
| 🟢 Baja | Variable `path` como string | 3,13 | Consistencia de tipos |
| 🟢 Baja | `get_cmap` deprecado | 33 | Compatibilidad futura |
| 🟢 Baja | Falta sección de conclusiones | — | Completitud |

---

## 6. Conclusión

El notebook está **bien estructurado en su lógica general** y produce resultados correctos para el análisis exploratorio. Los problemas principales son:

1. **Un error de estructura importante:** código Python que quedó en una celda Markdown y no se ejecuta (celda 16), con la sección 7 perdida.
2. **Omisiones de validación** que podrían ocultar problemas en los datos (rangos, splits duplicados, imágenes sin anotaciones).
3. **Mejoras menores** de mantenibilidad (importaciones, warnings, deprecaciones).

Se recomienda abordar primero los problemas de prioridad alta (🔴) para asegurar la integridad del notebook, y luego iterar sobre las mejoras de prioridad media y baja.
