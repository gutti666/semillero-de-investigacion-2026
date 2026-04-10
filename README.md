# Semillero de Investigación 2026
Repositorio del semillero enfocado en proyectos de ciencia de datos y machine learning aplicados a análisis de datos biológicos.

## Descripción

Actualmente el proyecto incluye un notebook de análisis preliminar para el dataset **High-Throughput Algae Cell Detection** (formato YOLO), con exploración de estructura, carga de anotaciones y visualización de resultados.

## Cronograma del Proyecto

```mermaid
gantt
    title Fase 1: Auditoría de Datos y Diagnóstico de Sensores | 11/02/26 | 17/03/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 1
    Arranque y Definición de Líneas de Investigación :done, 02/11/26, 02/17/26
        Configuración del Entorno Inicial :02/11/26, 02/12/26
        Ingesta y Estructuración :02/13/26, 02/14/26
        Definición de Objetivos Tabulares :02/15/26, 02/17/26

    section Semana 2
    Análisis Exploratorio (EDA) y Relaciones Espectrales :done, 02/18/26, 02/24/26
        Creación del repositorio documentado inicial 1.0 :02/18/26, 02/19/26
        Análisis de Correlación Multivariable :02/20/26, 02/21/26
        Auditoría de Variables de Color :02/22/26, 02/22/26
        Visualización de Tendencias :02/23/26, 02/24/26
   
    section Semana 3
    Diagnóstico de Viabilidad :done, 02/25/26, 03/03/26
        Evaluación de Redundancia Térmica :02/25/26, 02/27/26
        Control de Calidad de Sensores :02/28/26, 03/01/26
        Hito Técnico :03/02/26, 03/03/26

    section Semana 4
    Análisis de Continuidad Temporal y Alineación :done, 03/04/26, 03/10/26
        Auditoría de Timestamps :03/04/26, 03/05/26
        Intento de Sincronización :03/06/26, 03/07/26
        Análisis de Nulos :03/07/26, 03/10/26

    section Semana 5
    Conclusión de Inviabilidad y Cierre de Línea Tabular :done, 03/11/26, 03/17/26
        Evaluación de Riesgo de Imputación :03/11/26, 03/12/26
        Diagnóstico Final de Clasificación :03/13/26, 03/14/26
        Informe de Cierre de Fase :03/15/26, 03/17/26

```
```mermaid
gantt
    title Fase 2: Crisis de Integridad y Cambio de Paradigma | 18/03/26 | 31/03/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %%excludes weekends

    section Semana 6
    Reestructuración Estratégica :done, 03/18/26, 03/20/26
        Desvinculación de los datasets de sensores por Complejidad Insostenible y Baja Calidad :03/18/26, 03/20/26
        Pivotaje - Adopción del dataset High-Throughput Algae Cell Detection :03/18/26, 03/20/26

    section Semana 7
    Reconfiguración del proyecto :done, 03/21/26, 03/25/26
        Reconfiguración del Repositorio Documentado 2.0 :03/21/26, 03/21/26
        Diseño del Cronograma Final :03/22/26, 03/23/26
        Estudio de las 6 nuevas clases de microalgas :03/24/26, 03/24/26
        Revisión de soluciones y arquitecturas :03/25/26, 03/25/26
            YOLO (detección multiclase en tiempo real) :03/25/26, 03/25/26
            CNN (clasificación de imágenes) :03/25/26, 03/25/26
            SVM (clasificación supervisada) :03/25/26, 03/25/26
            LSTM (series temporales para crecimiento) :03/25/26, 03/25/26
            U-Net (segmentación de imágenes) :03/25/26, 03/25/26
            Faster R-CNN (red neuronal convolucional basada en regiones) :03/25/26, 03/25/26
            Comparación preliminar de ventajas y limitaciones de cada enfoque :03/25/26, 03/25/26

    section Semana 8
    Estudio y análisis del nuevo dataset :done, 03/26/26, 03/31/26
        Replicación técnica en Jupyter Notebook :03/26/26, 03/27/26
            Descarga y organización del dataset Kaggle :03/26/26, 03/27/26
            Limpieza inicial de datos :03/26/26, 03/27/26
            Train–test split :03/26/26, 03/27/26
        Análisis exploratorio profundo (EDA) :03/28/26, 03/29/26
            Distribución de clases (balance/desbalance) :03/28/26, 03/29/26
            Identificación de nulos, duplicados y rangos inválidos :03/28/26, 03/29/26
            Visualización de ejemplos por clase :03/28/26, 03/29/26
            Estudio de variabilidad morfológica y condiciones de captura :03/28/26, 03/29/26
        Informe de cierre de fase :03/30/26, 03/31/26
            Registro de hallazgos iniciales :03/30/26, 03/31/26
            Informe exploratorio preliminar :03/30/26, 03/31/26
```
```mermaid
gantt
    title Fase 3: Profundizacion y sintesis del analisis del dataset | 01/04/26 | 27/04/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 9
    Consolidacion del analisis inicial :active, 04/01/26, 04/06/26
        Sistematizacion de resultados del EDA realizado en marzo :04/01/26, 04/02/26
        Organizacion de hallazgos en tablas y graficas comparativas :04/03/26, 04/04/26
        Redaccion de resumen tecnico sobre variabilidad morfologica :04/05/26, 04/06/26

    section Semana 10 
    Evaluacion de calidad y problemas persistentes :active, 04/07/26, 04/13/26
        Evaluacion de calidad de anotaciones YOLO :04/07/26, 04/08/26
        Identificacion de problemas persistentes :04/09/26, 04/10/26
        Documentacion de criterios de calidad para preprocesamiento :04/11/26, 04/13/26

    section Semana 11
    Comparacion de arquitecturas y propuestas iniciales :active, 04/14/26, 04/20/26
        Comparacion exploratoria de arquitecturas revisadas :04/14/26, 04/17/26
        Seleccion de YOLO como arquitectura principal - nucleo :04/17/26, 04/17/26
        Definicion de roles complementarios de CNN, SVM, LSTM y Prophet :04/18/26, 04/20/26
        Propuesta inicial de mejoras en el enfoque de deteccion :04/18/26, 04/20/26

    section Semana 12
    Informe exploratorio y conclusiones :active, 04/21/26, 04/27/26
        Redaccion del informe exploratorio completo del dataset :04/21/26, 04/22/26
        Aplicacion del metodo cientifico hipotesis experimentacion inicial resultados preliminares :04/23/26, 04/24/26
        Conclusiones y alcances de la fase de analisis :04/25/26, 04/26/26
        Informe cierre de fase :04/27/26, 04/27/26

```
```mermaid
gantt
    title Fase 4: Preprocesamiento de datos | 28/04/26 | 25/05/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 13
    Limpieza avanzada y normalización :active, 04/28/26, 05/04/26
        Aplicar técnicas de limpieza avanzada :04/28/26, 04/30/26
        Normalización de imágenes y etiquetas :05/01/26, 05/02/26
        Validación inicial del dataset limpio :05/03/26, 05/04/26

    section Semana 14
    Data augmentation y balance de clases :active, 05/05/26, 05/11/26
        Técnicas de aumento de datos (rotación, escalado, recortes, iluminación) :05/05/26, 05/06/26
        Oversampling de clases minoritarias :05/07/26, 05/08/26
        Augmentations específicos para objetos pequeños :05/08/26, 05/09/26
        Documentación de resultados :05/10/26, 05/11/26

    section Semana 15
    Ajuste de etiquetas y diccionario técnico :active, 05/12/26, 05/18/26
        Revisión y ajuste de anotaciones YOLO :05/12/26, 05/13/26
        Construcción de diccionario técnico de variables y clases :05/14/26, 05/16/26
        Validación de consistencia entre imágenes y anotaciones :05/17/26, 05/18/26

    section Semana 16
    Validación final del dataset preprocesado :active, 05/19/26, 05/25/26
        Validación integral del dataset :05/19/26, 05/20/26
        Generación de métricas de calidad del dataset :05/21/26, 05/22/26
        Preparación del dataset definitivo para entrenamiento YOLO :05/23/26, 05/24/26
        Informe de cierre de fase de preprocesamiento :05/25/26, 05/25/26
```
```mermaid
gantt
    title Fase 5: Modelado predictivo | 26/05/26 | 22/06/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 17
    Implementación de modelos de regresión :active, 05/26/26, 06/01/26
        Configuración del entorno de entrenamiento :05/26/26, 05/26/26
        Regresión lineal y polinómica para estimar crecimiento de microalgas :05/27/26, 05/29/26
        Evaluación inicial de desempeño con métricas de error (RMSE, MAE) :05/30/26, 06/01/26

    section Semana 18
    Random Forest y XGBoost :active, 06/02/26, 06/08/26
        Entrenamiento de modelos Random Forest para predicción multivariable :06/02/26, 06/03/26
        Implementación de XGBoost para mejorar precisión en escenarios complejos :06/04/26, 06/06/26
        Comparación de resultados entre regresión, Random Forest y XGBoost :06/07/26, 06/08/26

    section Semana 19
    Modelado de series temporales :active, 06/09/26, 06/15/26
        Implementación de LSTM para predicción de crecimiento en secuencias temporales :06/09/26, 06/11/26
        Uso de Prophet para tendencias de largo plazo :06/12/26, 06/13/26
        Validación cruzada de modelos de series temporales :06/14/26, 06/15/26

    section Semana 20
    Comparación y selección de modelos :active, 06/16/26, 06/22/26
        Comparación integral de todos los modelos predictivos :06/16/26, 06/18/26
        Selección del modelo más robusto para crecimiento de microalgas :06/19/26, 06/19/26
        Informe cierre de fase :06/20/26, 06/22/26
```
```mermaid
gantt
    title Fase 6: Modelado de clasificación (estado fisiológico) | 23/06/26 | 20/07/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 21
    Entrenamiento inicial con YOLO :active, 06/23/26, 06/29/26
        Configuración del entorno de entrenamiento para clasificación multiclase :06/23/26, 06/23/26
        Entrenamiento inicial del modelo YOLO (transfer learning, fine-tuning, anchor boxes, métricas mAP/IoU) :06/24/26, 06/26/26
        Evaluación preliminar con métricas de precisión y recall :06/27/26, 06/29/26

    section Semana 22
    Comparación con CNN y SVM :active, 06/30/26, 07/06/26
        Implementación de CNN para clasificación de imágenes :06/30/26, 07/02/26
        Entrenamiento de SVM sobre características extraídas :07/03/26, 07/04/26
        Comparación de resultados YOLO vs CNN vs SVM :07/05/26, 07/06/26

    section Semana 23
    Optimización de YOLO :active, 07/07/26, 07/13/26
        Ajuste de hiperparámetros para mejorar detección de objetos pequeños :07/07/26, 07/09/26
        Estrategias para reducir impacto de desenfoque por movimiento :07/10/26, 07/11/26
        Manejo de fondos complejos mediante técnicas de regularización :07/12/26, 07/13/26

    section Semana 24
    Selección del modelo más robusto :active, 07/14/26, 07/20/26
        Comparación integral de desempeño entre YOLO optimizado, CNN y SVM :07/14/26, 07/15/26
        Selección del modelo más robusto para clasificación multiclase :07/16/26, 07/17/26
        Informe cierre de fase :07/18/26, 07/20/26
```
```mermaid
gantt
    title Fase 7: Evaluación y optimización final | 21/07/26 | 31/08/26 |
    dateFormat MM/DD/YY
    axisFormat %m/%d
    %% excludes weekends

    section Semana 25
    Evaluación integral de modelos :active, 07/21/26, 07/27/26
        Evaluación de desempeño de los modelos seleccionados (YOLO, predictor de crecimiento) :07/21/26, 07/23/26
        Validación cruzada con dataset completo :07/24/26, 07/25/26
        Análisis de métricas de precisión, recall, F1-score y error de predicción :07/26/26, 07/27/26

    section Semana 26
    Optimización de hiperparámetros :active, 07/28/26, 08/03/26
        Ajuste de hiperparámetros en YOLO, anchor boxes y modelos predictivos :07/28/26, 07/29/26
        Implementación de técnicas de regularización y reducción de sobreajuste :07/30/26, 08/01/26
        Documentación de mejoras obtenidas :08/02/26, 08/03/26

    section Semana 27
    Robustez y generalización :active, 08/04/26, 08/10/26
        Pruebas de robustez en condiciones adversas (objetos pequeños, desenfoque, fondos complejos) :08/04/26, 08/06/26
        Evaluación de generalización en escenarios distintos :08/07/26, 08/08/26
        Informe de robustez y generalización :08/09/26, 08/10/26

    section Semana 28
    Integración y documentación final :active, 08/11/26, 08/17/26
        Integración de modelos seleccionados en flujo de trabajo unificado :08/11/26, 08/12/26
        Documentación técnica completa del proyecto :08/13/26, 08/14/26
        Preparación de informe final para el semillero :08/15/26, 08/17/26

    section Semana 29
    Presentación y cierre :active, 08/18/26, 08/31/26
        Elaboración de presentación de resultados :08/18/26, 08/25/26
        Socialización de hallazgos con el semillero :08/26/26, 08/27/26
        Informe final de cierre del proyecto :08/28/26, 08/31/26
```



## Configuración del Entorno

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Jupyter Notebook
- Cuenta de Kaggle con acceso al dataset
- Dataset local en `nuevo-dataset/high-throughput-algae-cell-detection` (descarga automática o manual)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/gutti666/semillero-de-investigacion-2026.git
   cd semillero-de-investigacion-2026
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv .venv
   
   # En Windows
   .venv\Scripts\activate
   
   # En Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencias Principales

Las librerías principales utilizadas en este proyecto son:

- **pandas**: Manipulación y análisis de datos
- **numpy**: Computación numérica
- **matplotlib**: Visualización de datos
- **seaborn**: Visualización estadística
- **jupyter**: Entorno de notebooks interactivos
- **scikit-learn**: Machine learning (opcional)

El notebook de `nuevo-dataset` también usa:

- **Pillow**: Lectura y manejo de imágenes
- **PyYAML**: Lectura del archivo de configuración `data.yaml`
- **kagglehub**: Descarga del dataset desde Kaggle

Para instalar manualmente las dependencias básicas:

```bash
pip install pandas numpy matplotlib seaborn jupyter pillow pyyaml kagglehub
```

### Preparación del Dataset

El notebook incluye una celda inicial que intenta descargar el dataset y copiarlo en la ruta estándar del repositorio:

`nuevo-dataset/high-throughput-algae-cell-detection`

#### Opción A: Descarga automática (recomendada)

1. Configurar credenciales de Kaggle.
2. Ejecutar la celda de preparación del dataset en el notebook.
3. Verificar que exista la carpeta `nuevo-dataset/high-throughput-algae-cell-detection`.

#### Opción B: Carga manual (si falla red o DNS)

Si aparece un error de conexión con `api.kaggle.com`:

1. Descargar el dataset manualmente desde Kaggle en un entorno con internet.
2. Copiar la carpeta descargada en `nuevo-dataset/high-throughput-algae-cell-detection`.
3. Reejecutar la celda de preparación para validar ruta y continuar.

## Uso

### Iniciar Jupyter Notebook

1. Activar el entorno virtual (si se creó uno)
2. Ejecutar el siguiente comando:
   ```bash
   jupyter notebook
   ```
3. El navegador se abrirá automáticamente con la interfaz de Jupyter
4. Abrir el archivo `nuevo-dataset/inicialización_datos_nuevodataset.ipynb` para comenzar

### Flujo del Notebook de Nuevo Dataset

El notebook `nuevo-dataset/inicialización_datos_nuevodataset.ipynb` incluye:

- Importación de librerías básicas
- Configuración de visualización
- Configuración de pandas
- Verificación de versiones
- Exploración de la estructura del dataset local
- Carga de configuración YOLO desde `data.yaml`
- Construcción de un DataFrame de anotaciones (`split`, `class_id`, `x_center`, `y_center`, `width`, `height`, `area`, `aspect_ratio`)
- Estadísticas descriptivas y validación de datos faltantes
- Análisis visual preliminar:
  - Distribución de clases (total y por split)
  - Distribución de dimensiones de bounding boxes
  - Distribución espacial de centros
  - Número de anotaciones por imagen
  - Matriz de correlación de variables geométricas
  - Muestras de imágenes con bounding boxes superpuestos

### Estructura Esperada del Dataset

El notebook detecta de forma automática la ruta del dataset y soporta la estructura anidada actual:

```text
nuevo-dataset/
└── high-throughput-algae-cell-detection/
   └── versions/
      └── 3/
         ├── data.yaml
         ├── train/
         │   └── train/
         │       ├── images/
         │       └── labels/
         └── test/
            └── test/
               ├── images/
               └── labels/
```

Para ubicar los datos, el notebook escanea carpetas `labels` de forma recursiva y las empareja con su carpeta hermana `images`.

## Estructura del Proyecto

```
semillero-de-investigacion-2026/
├── README.md
├── requirements.txt
├── datos/
├── docs/
└── nuevo-dataset/
   ├── inicialización_datos_nuevodataset.ipynb
   └── high-throughput-algae-cell-detection/
```

## Contribuir

Si deseas contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Recursos Adicionales

- [Documentación de Pandas](https://pandas.pydata.org/docs/)
- [Documentación de NumPy](https://numpy.org/doc/)
- [Documentación de Matplotlib](https://matplotlib.org/stable/contents.html)
- [Documentación de Seaborn](https://seaborn.pydata.org/)
- [Guía de Jupyter](https://jupyter-notebook.readthedocs.io/)

## Licencia

Este proyecto es parte del semillero de investigación de Ingeniería de Sistemas 2026.
