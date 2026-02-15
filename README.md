# Semillero de Investigación 2026
Este repositorio se enfocará en temas de semillero de investigación - Ingeniería de sistemas

## Descripción

Repositorio dedicado a proyectos de ciencia de datos y machine learning del semillero de investigación.

## Configuración del Entorno

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Jupyter Notebook

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/gutti666/semillero-de-investigacion-2026.git
   cd semillero-de-investigacion-2026
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
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

Para instalar manualmente las dependencias básicas:

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

## Uso

### Iniciar Jupyter Notebook

1. Activar el entorno virtual (si se creó uno)
2. Ejecutar el siguiente comando:
   ```bash
   jupyter notebook
   ```
3. El navegador se abrirá automáticamente con la interfaz de Jupyter
4. Abrir el archivo `inicializacion_basica.ipynb` para comenzar

### Estructura del Notebook de Inicialización

El notebook `inicializacion_basica.ipynb` incluye:

- Importación de librerías básicas
- Configuración de visualización
- Configuración de pandas
- Verificación de versiones
- Ejemplos básicos de análisis de datos
- Funciones útiles predefinidas

## Estructura del Proyecto

```
semillero-de-investigacion-2026/
├── README.md                      # Este archivo
├── inicializacion_basica.ipynb   # Notebook de inicialización
├── requirements.txt              # Dependencias del proyecto
└── datos/                        # Directorio para datasets (crear según necesidad)
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
