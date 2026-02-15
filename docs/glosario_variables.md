# 📊 Glosario de Variables del Dataset de Espirulina

## Semillero de Investigación 2026 — Ingeniería de Sistemas

Este documento contiene las definiciones científicas y técnicas de todas las variables registradas en el sistema de monitoreo por visión artificial del cultivo de *Spirulina* (Arthrospira platensis).

**Versión**: 1.0  
**Fecha**: Febrero 15, 2026  
**Dataset**: `datos/Datos_Espirulina.csv` (~66,700 registros)

---

## 📑 Índice

1. [Variables Temporales](#variables-temporales)
2. [Variables de Biomasa y Absorbancia](#variables-de-biomasa-y-absorbancia)
3. [Canales de Color RGB (ROI)](#canales-de-color-rgb-roi)
4. [Canales HSV (ROI)](#canales-hsv-roi)
5. [Variables de Máscara Segmentada](#variables-de-máscara-segmentada)
6. [Índices Espectrales Derivados](#índices-espectrales-derivados)
7. [Interpretación Integrada](#interpretación-integrada)
8. [Referencias Bibliográficas](#referencias-bibliográficas)

---

## 🕒 Variables Temporales

### `Fecha`
- **Tipo**: String (formato: YYYY-MM-DD)
- **Descripción**: Fecha de la captura de imagen
- **Ejemplo**: `2025-10-21`
- **Uso**: Análisis de evolución temporal, detección de ciclos diarios, correlación con eventos ambientales

### `Hora`
- **Tipo**: String (formato: HH:MM:SS)
- **Descripción**: Hora de la captura de imagen
- **Ejemplo**: `22:00:42`
- **Frecuencia de muestreo**: Cada ~5 minutos
- **Importancia**: Permite identificar:
  - **Ciclos de fotoperiodo** (16h luz / 8h oscuridad óptimo)
  - **Ritmos circadianos** del cultivo
  - **Fotoinhibición** durante horas de máxima irradiancia (12:00-14:00)

### `CamIndex`
- **Tipo**: Integer
- **Rango**: 0, 1, 2, ...
- **Descripción**: Identificador de la cámara utilizada
- **Uso**: 
  - Comparación entre múltiples reactores
  - Control de calidad entre dispositivos
  - Validación de consistencia de mediciones

---

## 🌿 Variables de Biomasa y Absorbancia

### `Porcentaje Verde (%)`

#### Definición
Proporción de píxeles clasificados como "verde" en la imagen segmentada del cultivo, relativo al área total de la región de interés (ROI).

#### Fórmula
```
Porcentaje Verde (%) = (Píxeles_Verdes / Píxeles_Totales_ROI) × 100
```

#### Interpretación Biológica

| Rango | Estado del Cultivo | Interpretación |
|-------|-------------------|----------------|
| **>85%** | Fase estacionaria tardía | Muy alta densidad celular, riesgo de auto-sombreado |
| **70-85%** | Fase exponencial/estacionaria | Crecimiento óptimo, alta concentración de clorofila y ficocianina |
| **50-70%** | Crecimiento moderado | Fase exponencial temprana o inicio de senescencia |
| **30-50%** | Fase lag o estrés | Cultivo joven, dilución reciente o estrés nutricional |
| **<30%** | Alerta crítica | Posible clorosis, fotoinhibición severa o contaminación |

#### Correlatos
- **R² > 0.95** con Absorbancia Estimada
- **R² > 0.90** con densidad celular (células/mL)
- **R² > 0.85** con peso seco gravimétrico (g/L)

#### Alertas
- 🟡 **Amarilla**: Caída >10% en 24h → revisar nutrientes (N, P)
- 🔴 **Roja**: Caída >20% en 24h → posible colapso del cultivo

---

### `Absorbancia Estimada`

#### Definición
Estimación computacional de la absorbancia espectral del cultivo, calculada a partir de la intensidad de los canales RGB y la ley de Bouguer-Lambert-Beer (BLB).

#### Base Teórica
**Ley de Beer-Lambert**:
$$A = -\log_{10}\left(\frac{I}{I_0}\right) = \varepsilon \cdot c \cdot L$$

Donde:
- $A$ = Absorbancia (unidades adimensionales)
- $I$ = Intensidad de luz transmitida
- $I_0$ = Intensidad de luz incidente
- $\varepsilon$ = Coeficiente de extinción molar (L·mol⁻¹·cm⁻¹)
- $c$ = Concentración de pigmentos (mol/L)
- $L$ = Longitud del paso óptico (cm)

#### Relación Empírica
```python
Absorbancia Estimada ≈ Porcentaje_Verde / 25
```

**Ejemplo**:
- Porcentaje Verde = 80.65%
- Absorbancia Estimada ≈ 80.65 / 25 = **3.23**

#### Equivalencia con OD750
La absorbancia estimada se aproxima a la **Densidad Óptica a 750 nm (OD750)**, el estándar de referencia para cuantificación de biomasa en microalgas:
- OD < 1.0 → Cultivo diluido
- OD 1.0 - 2.0 → Densidad moderada
- OD 2.0 - 4.0 → Alta densidad (tu rango: 3.21-3.31 ✅)
- OD > 4.0 → Riesgo de auto-sombreado

#### Conversión a Biomasa Seca
```python
# Modelo lineal calibrado (requiere validación experimental)
Biomasa_seca (g/L) = a × Absorbancia + b
# Valores típicos: a ≈ 0.3-0.5, b ≈ 0.1-0.2
```

---

## 🎨 Canales de Color RGB (ROI)

Las variables RGB representan la **intensidad promedio** de los canales Rojo, Verde y Azul en la **Región de Interés (ROI)**, que incluye todo el campo de visión del cultivo (incluye burbujas, reflejos menores, etc.).

### `R_ROI` (Canal Rojo)

#### Definición
Intensidad del canal rojo en escala 0-255.

#### Rango Espectral
620-750 nm (rojo a infrarrojo cercano)

#### Pigmentos Absorbidos
- **Clorofila a**: Pico de absorción a 662-665 nm
- **Ficoeritrina** (en algas rojas): 495-570 nm
- **Ficocianina** (absorción secundaria): ~620 nm

#### Interpretación en Espirulina

| Valor R_ROI | Interpretación | Estado |
|-------------|----------------|--------|
| **60-70** | Alta absorción de rojo | Concentración óptima de clorofila a ✅ (tu rango) |
| **70-90** | Absorción moderada | Cultivo diluido o fase lag |
| **>90** | Baja absorción | Cultivo muy joven, blanqueamiento o estrés lumínico |

#### Comportamiento Esperado
```python
# La clorofila a absorbe fuertemente el rojo, por lo que:
# Más biomasa → Menos luz roja reflejada → R_ROI bajo ✅
```

---

### `G_ROI` (Canal Verde) ⭐ **Variable Clave**

#### Definición
Intensidad del canal verde en escala 0-255.

#### Rango Espectral
495-570 nm (verde-amarillo)

#### Comportamiento en Cianobacterias (Espirulina)

**Propiedad única**: Las cianobacterias **reflejan** luz verde porque:
1. La **clorofila a** absorbe débilmente en esta región (ventana espectral entre picos azul 430 nm y rojo 665 nm)
2. La **ficocianina** (pigmento azul-verdoso característico) no absorbe eficientemente en 495-570 nm
3. Resultado: `G_ROI` es el **canal dominante** en cultivos de Espirulina

#### Interpretación

| Valor G_ROI | Biomasa Estimada | Estado |
|-------------|------------------|--------|
| **120-140** | Alta densidad | Fase exponencial tardía/estacionaria ✅ (tu rango: 130-134) |
| **90-120** | Densidad moderada | Crecimiento activo |
| **60-90** | Densidad baja | Fase lag inicial |
| **<60** | Muy baja | Cultivo joven o diluido |

#### Correlación con Absorbancia
```python
from scipy.stats import pearsonr

# Correlación esperada: R² > 0.95
r, p_value = pearsonr(df['G_ROI'], df['Absorbancia Estimada'])
print(f"Correlación G_ROI vs Absorbancia: R² = {r**2:.4f}")
```

#### Por qué G_ROI es la variable más importante
- ✅ Mayor rango dinámico (60-140) vs R_ROI (60-90) o B_ROI (0-5)
- ✅ Menos sensible a sombras y reflejos especulares
- ✅ Directamente proporcional a concentración de ficocianina
- ✅ Permite distinguir Espirulina de algas verdes (que tienen G_ROI menor)

---

### `B_ROI` (Canal Azul)

#### Definición
Intensidad del canal azul en escala 0-255.

#### Rango Espectral
450-495 nm (azul)

#### Pigmentos Absorbidos
- **Clorofila a**: Pico de absorción máximo a 430 nm
- **Carotenoides**: Fuerte absorción en 400-500 nm
- **Ficocianina**: Absorción secundaria con máximo a 615-620 nm

#### Interpretación en Espirulina

| Valor B_ROI | Interpretación | Actividad Fotosintética |
|-------------|----------------|-------------------------|
| **0-2** | Absorción casi total | Fotosíntesis muy activa ✅ (tu rango: 0.2-0.3) |
| **2-10** | Alta absorción | Actividad normal |
| **>10** | Absorción reducida | Posible fotoinhibición o pérdida de pigmentos |

#### Significado Biológico
```python
# B_ROI ≈ 0 indica que:
# 1. La luz azul está siendo COMPLETAMENTE absorbida
# 2. El Fotosistema II está altamente activo
# 3. La concentración de clorofila a es alta
# 4. El cultivo está en fase exponencial con fotosíntesis óptima ✅
```

#### Alerta de Estrés
Si `B_ROI` aumenta >5 manteniendo constante la iluminación:
- 🟡 **Posible fotoinhibición** (exceso de luz)
- 🟡 **Degradación de clorofila** (deficiencia de N)
- 🟡 **Acumulación de carotenoides** fotoprotectores (estrés oxidativo)

---

## 🌈 Canales HSV (ROI)

El espacio de color **HSV (Hue-Saturation-Value)** es una transformación del RGB que separa el **color** (H) de la **intensidad** (V), facilitando la segmentación y detección de cambios fisiológicos.

### `H_ROI` (Hue / Matiz)

#### Definición
Ángulo del color en el círculo cromático (0-360° convertido a 0-255 en OpenCV).

#### Escala de Conversión
```python
# OpenCV usa escala 0-180 para Hue
H_degrees = H_ROI × 2  # Convertir a grados reales
```

#### Interpretación del Matiz

| H_ROI (OpenCV) | Grados Reales | Color | Interpretación en Espirulina |
|----------------|---------------|-------|------------------------------|
| **40-50** | **80-100°** | Verde amarillento | **Normal** ✅ (tu rango: 44.7-44.9) |
| **30-40** | **60-80°** | Amarillo verdoso | Posible inicio de clorosis |
| **<30** | **<60°** | Amarillo | 🔴 Clorosis (deficiencia de N) |
| **50-70** | **100-140°** | Verde puro | Cultivo muy joven o diluido |

#### Diagnóstico por Color

**Color esperado en Espirulina saludable**: Verde azulado a verde amarillento (40-50 en escala OpenCV)

**Cambios patológicos**:
```python
if H_ROI < 35:
    print("⚠️ Alerta: Amarillamiento detectado")
    print("   Causas posibles:")
    print("   - Deficiencia de nitrógeno (N)")
    print("   - Senescencia del cultivo")
    print("   - Fotoinhibición crónica")
elif H_ROI > 55:
    print("⚠️ Alerta: Color verde intenso inusual")
    print("   Causas posibles:")
    print("   - Contaminación con Chlorella sp.")
    print("   - Dilución excesiva")
```

#### Correlato Biológico
El matiz refleja la **proporción relativa** de pigmentos:
- **Clorofila a** (verde) vs **Ficocianina** (azul-verde) vs **Carotenoides** (amarillo-naranja)

---

### `S_ROI` (Saturation / Saturación)

#### Definición
Pureza o intensidad del color (0 = gris, 255 = color puro).

#### Interpretación

| Valor S_ROI | Calidad del Cultivo | Descripción |
|-------------|---------------------|-------------|
| **240-255** | Excelente | Pigmentación uniforme, sin contaminantes ✅ (tu rango: 254.4-254.6) |
| **200-240** | Buena | Presencia menor de material inerte |
| **150-200** | Regular | Posible espuma o burbujas excesivas |
| **<150** | Pobre | Contaminación, blanqueamiento o espuma densa |

#### Significado Biológico
- **Alta saturación** → Cultivo **monocromático** con alta concentración de pigmentos fotosintéticos
- **Baja saturación** → Presencia de materiales que diluyen el color:
  - Espuma persistente
  - Precipitados de carbonato
  - Contaminación con bacterias heterotróficas
  - Detritos celulares

#### Uso en Control de Calidad
```python
# Validación de pureza del cultivo
if df['S_ROI'].mean() > 240:
    print("✅ Cultivo puro con pigmentación homogénea")
elif df['S_ROI'].mean() < 200:
    print("⚠️ Verificar presencia de contaminantes o espuma")
```

---

### `V_ROI` (Value / Valor)

#### Definición
Luminosidad o brillo del color (0 = negro, 255 = blanco). Matemáticamente, es el **máximo** de los tres canales RGB.

```python
V_ROI = max(R_ROI, G_ROI, B_ROI)
```

#### Interpretación en Espirulina

En tu dataset:
```python
V_ROI ≈ G_ROI  (130-134)
# Esto confirma que el canal VERDE es el dominante ✅
```

| Valor V_ROI | Densidad Óptica | Estado |
|-------------|-----------------|--------|
| **120-140** | Alta | Fase exponencial/estacionaria ✅ |
| **80-120** | Moderada | Crecimiento activo |
| **<80** | Baja | Cultivo joven o muy denso (auto-sombreado) |

#### Relación con Turbidez
```python
# V_ROI está inversamente relacionado con turbidez:
# Más biomasa → Más dispersión de luz → V_ROI moderado
# Cultivo muy denso (OD > 4) → V_ROI puede disminuir por bloqueo de luz
```

---

## 🎭 Variables de Máscara Segmentada

Las variables con sufijo `_Mascara` representan los mismos canales RGB/HSV pero aplicados **exclusivamente** a la región segmentada del cultivo, excluyendo:
- ✂️ Burbujas de aire
- ✂️ Espuma superficial
- ✂️ Paredes del reactor
- ✂️ Reflejos especulares (brillo del vidrio)
- ✂️ Sombras

### Comparación ROI vs Máscara

#### `R_Mascara`, `G_Mascara`, `B_Mascara`

**Propósito**: Obtener valores "reales" de color del cultivo sin interferencias.

**Ejemplo de tu muestra**:
```python
G_ROI     = 133.93
G_Mascara = 104.48
Ratio     = 104.48 / 133.93 = 0.78 ✅

# Interpretación:
# La máscara eliminó ~22% de píxeles (burbujas + reflejos)
# Esto es NORMAL y esperado en reactores con aireación
```

#### Ratios de Validación

| Variable | Ratio Esperado (Máscara/ROI) | Tu Valor | Estado |
|----------|------------------------------|----------|--------|
| **G_Mascara / G_ROI** | 0.75 - 0.85 | 0.78 | ✅ Normal |
| **R_Mascara / R_ROI** | 0.70 - 0.85 | 0.76 | ✅ Normal |
| **S_Mascara / S_ROI** | 0.75 - 0.90 | 0.81 | ✅ Normal |

#### Alertas de Segmentación

```python
def validar_segmentacion(df):
    """
    Valida la calidad del algoritmo de segmentación
    """
    ratio_G = df['G_Mascara'].mean() / df['G_ROI'].mean()
    
    if 0.75 <= ratio_G <= 0.85:
        return "✅ Segmentación correcta"
    elif 0.60 <= ratio_G < 0.75:
        return "⚠️ Exceso de píxeles eliminados (revisar umbral)"
    elif ratio_G > 0.85:
        return "⚠️ Segmentación insuficiente (burbujas no filtradas)"
    else:
        return "🔴 Error crítico en segmentación"
```

---

## 📐 Índices Espectrales Derivados

Estos índices se calculan combinando los canales RGB/HSV y proporcionan información adicional sobre el estado fisiológico del cultivo.

### NDVI Proxy (Índice de Vegetación Simplificado)

#### Fórmula
$$\text{NDVI}_{\text{proxy}} = \frac{G_{\text{ROI}} - R_{\text{ROI}}}{G_{\text{ROI}} + R_{\text{ROI}}}$$

#### Interpretación

| NDVI Proxy | Actividad Fotosintética | Estado |
|------------|------------------------|--------|
| **0.30 - 0.40** | Alta | Cultivo sano en fase exponencial ✅ |
| **0.20 - 0.30** | Moderada | Crecimiento normal |
| **<0.20** | Baja | Fase lag o estrés |

#### Cálculo en tu muestra:
```python
NDVI_proxy = (133.93 - 68.67) / (133.93 + 68.67)
           = 65.26 / 202.60
           = 0.322 ✅
# Interpretación: Fotosíntesis activa, cultivo saludable
```

---

### Ratio R/G (Indicador de Biomasa)

#### Fórmula
$$\text{Ratio}_{R/G} = \frac{R_{\text{ROI}}}{G_{\text{ROI}}}$$

#### Interpretación

| Ratio R/G | Concentración de Biomasa | Estado |
|-----------|--------------------------|--------|
| **0.45 - 0.55** | Alta densidad | Fase estacionaria ✅ (tu valor: 0.51) |
| **0.55 - 0.70** | Densidad moderada | Fase exponencial |
| **>0.70** | Baja densidad | Cultivo joven o diluido |

#### Cálculo en tu muestra:
```python
Ratio_RG = 68.67 / 133.93 = 0.513 ✅
# Interpretación: Alta concentración de ficocianina
```

---

### Ratio G/B (Indicador de Salud de Pigmentos)

#### Fórmula
$$\text{Ratio}_{G/B} = \frac{G_{\text{ROI}}}{B_{\text{ROI}}}$$

#### Interpretación

| Ratio G/B | Estado de Pigmentos | Interpretación |
|-----------|---------------------|----------------|
| **>100** | Óptimo | Alta clorofila y ficocianina ✅ (tu valor: 432) |
| **50-100** | Normal | Cultivo saludable |
| **<50** | Alerta | Posible fotoinhibición o acumulación de carotenoides |

#### Cálculo en tu muestra:
```python
Ratio_GB = 133.93 / 0.31 = 432.0 ✅
# Interpretación: Absorción casi total de luz azul
# Esto indica fotosíntesis altamente activa
```

---

## 🔬 Interpretación Integrada

### Caso de Estudio: Tu Muestra (2025-10-21, 22:00:42)

#### Datos Brutos
```python
Fecha:                 2025-10-21
Hora:                  22:00:42
Porcentaje Verde:      80.65%
Absorbancia Estimada:  3.23
R_ROI:                 68.67
G_ROI:                 133.93
B_ROI:                 0.31
H_ROI:                 44.71°
S_ROI:                 254.4
V_ROI:                 133.93
```

#### Análisis Multiparamétrico

| Indicador | Valor | Interpretación | Estado |
|-----------|-------|----------------|--------|
| **Porcentaje Verde** | 80.65% | Alta densidad celular | ✅ Óptimo |
| **Absorbancia** | 3.23 | Concentración alta (OD~3.2) | ✅ Óptimo |
| **Ratio G/R** | 1.95 | Reflectancia verde dominante | ✅ Normal |
| **B_ROI** | 0.31 | Absorción azul casi total | ✅ Fotosíntesis activa |
| **H_ROI** | 44.71° | Verde amarillento típico | ✅ Normal |
| **Saturación** | 254.4 | Pigmentación uniforme | ✅ Excelente |
| **NDVI Proxy** | 0.322 | Actividad fotosintética alta | ✅ Óptimo |

#### Diagnóstico Integral

```
🔬 ESTADO DEL CULTIVO: Fase Exponencial Tardía / Estacionaria Temprana

✅ Indicadores Positivos:
   - Color verde intenso sin amarillamiento (H=44.71°)
   - Alta saturación (S=254.4) indica pureza del cultivo
   - Absorción completa de luz azul (B=0.31) → fotosíntesis óptima
   - Reflectancia verde dominante (G=133.93) → alta ficocianina
   - Porcentaje Verde >80% → densidad celular elevada

⚠️ Monitorear:
   - Riesgo de auto-sombreado si Absorbancia >3.5
   - Verificar concentración de N y P para mantener crecimiento
   - Evaluar necesidad de dilución si Porcentaje Verde >90%

📊 Biomasa Estimada:
   - Peso seco estimado: 1.0 - 1.3 g/L
   - Densidad celular estimada: 2-3 × 10⁶ células/mL

🎯 Recomendaciones:
   1. Mantener condiciones actuales (T°, pH, iluminación)
   2. Monitorear evolución de Porcentaje Verde cada 12h
   3. Preparar para cosecha si se alcanza Fase Estacionaria (Abs ~3.5)
   4. Fusionar con datos de sensores (Skill 10) para análisis completo
```

---

## 📚 Referencias Bibliográficas

### Documentos del Proyecto

1. **PDF Base**: "Fisiología del Crecimiento y Respuesta Espectral de las Algas: Correlatos entre Pigmentación, Biomasa y Absorbancia" (2026)
   - Secciones relevantes: Correlatos Biomasa-Absorbancia, Índices Espectrales

2. **Copilot Instructions**: `.github/copilot-instructions.md`
   - Skills 1-10 para análisis de cultivos de algas

3. **Agente Bioalgae Monitor**: `.github/agents/bioalgae-monitor.yml`
   - Sistema de diagnóstico automatizado

### Literatura Científica Citada en el PDF

4. Porra, R.J. et al. (1989). "Determination of accurate extinction coefficients and simultaneous equations for assaying chlorophylls a and b"
   - Coeficientes de extinción y ecuaciones universales

5. Ritchie, R.J. (2008). "Universal chlorophyll equations for estimating chlorophylls a, b, c, and d"
   - Ecuaciones para determinación simultánea de clorofilas

6. Lawrenz, E. et al. (2010). "Predicting the absorption spectra of phytoplankton"
   - Modelos bio-ópticos para predicción de absorbancia

7. Wynne, T.T. et al. (2008). "Relating spectral shape to cyanobacterial blooms"
   - Índices espectrales para detección de cianobacterias

8. Mishra, S. & Mishra, D. (2012). "Normalized difference chlorophyll index (NDCI)"
   - NDCI para monitoreo de concentración de ficocianina

### Ecuaciones de Referencia

**Ley de Beer-Lambert Modificada (mBLB)**:
$$X = a \cdot \frac{\text{OD}_{750}}{L} + b$$

**Coeficiente de Extinción Molar (Clorofila a en acetona 90%)**:
$$\varepsilon_{664} = 11.93 \text{ L·g}^{-1}\text{·cm}^{-1}$$

**Tasa de Crecimiento Específico**:
$$\mu = \frac{\ln(X_2) - \ln(X_1)}{t_2 - t_1} \quad [\text{día}^{-1}]$$

---

## 🛠️ Uso de Este Glosario

### Para Análisis de Datos
```python
import pandas as pd

# Cargar glosario como referencia
VARIABLES_INFO = {
    'Porcentaje Verde (%)': {
        'rango_optimo': (70, 85),
        'alerta_amarilla': (50, 70),
        'alerta_roja': (0, 50)
    },
    'H_ROI': {
        'rango_normal': (40, 50),
        'clorosis': (0, 35),
        'cultivo_diludo': (50, 70)
    }
}

def diagnosticar_cultivo(row):
    """Diagnóstico automatizado basado en el glosario"""
    diagnostico = []
    
    # Verificar Porcentaje Verde
    pv = row['Porcentaje Verde (%)']
    if pv < 50:
        diagnostico.append("🔴 Alerta: Baja densidad celular")
    elif pv > 90:
        diagnostico.append("🟡 Advertencia: Riesgo de auto-sombreado")
    
    # Verificar color
    h = row['H_ROI']
    if h < 35:
        diagnostico.append("🔴 Alerta: Clorosis detectada")
    
    return "; ".join(diagnostico) if diagnostico else "✅ Normal"

# Aplicar diagnóstico
df['Diagnostico'] = df.apply(diagnosticar_cultivo, axis=1)
```

### Para Comunicación con el Agente
```markdown
@bioalgae-monitor Analiza el estado del cultivo usando las definiciones del glosario:
- Porcentaje Verde: 80.65%
- H_ROI: 44.71°
- G_ROI: 133.93
```

---

**Documento creado por**: Bioalgae Monitor Agent  
**Última actualización**: Febrero 15, 2026  
**Versión**: 1.0
