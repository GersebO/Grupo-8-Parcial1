# Análisis Exploratorio y Transformación de Datos de Urgencias Hospitalarias

**Grupo 8 - Programación para Ciencia de Datos**  
**Fecha:** 19 de abril de 2026  
**Dataset:** `urgencias_noprocesados_grupo08.csv`

## Descripción del Proyecto

Este proyecto realiza un análisis exploratorio y transformación de datos correspondiente a registros médicos de urgencias hospitalarias en Chile. El dataset contiene información sobre atenciones de urgencia, incluyendo variables demográficas, clasificación clínica (triage), causas de consulta, costos y geolocalización.

Los objetivos principales incluyen:
- Diagnosticar la calidad del dataset original.
- Limpiar y transformar los datos utilizando técnicas avanzadas con NumPy y Pandas.
- Validar la integridad de los datos resultantes.

El proyecto sigue una arquitectura modular con código reutilizable en el directorio `src/` e informes en `docs/`.

## Estructura del Proyecto

```
Grupo-8-Parcial1/
├── data/                          # Datos originales (no modificados)
│   └── urgencias_noprocesados_grupo08.csv
├── docs/                          # Informes y documentación
│   └── Informe_Tecnico_P1.md
├── notebooks/                     # Análisis en Jupyter Notebook
│   ├── 01_analisis_exploratorio.ipynb
│   └── 02_transformaciones_numpy.ipynb
├── outputs/                       # Gráficos generados automáticamente
│   ├── graficos_groupby.png
│   └── numpy_transformaciones.png
├── src/                           # Módulos Python reutilizables
│   ├── limpieza.py
│   ├── transformaciones.py
│   └── agregaciones.py
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Este archivo
└── venv/                          # Entorno virtual (opcional)
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.13.13 o superior
- Git (opcional, para clonar el repositorio)

### Instalación
1. Clona o descarga el repositorio.
2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   - Windows: `.\venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencias Principales
- pandas==2.x
- numpy==1.x
- matplotlib==3.x
- seaborn==0.x
- jupyter
- (Otras librerías según requirements.txt)

## Uso

### Ejecutar los Notebooks
1. Activa el entorno virtual.
2. Inicia Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Abre los notebooks en la carpeta `notebooks/`:
   - `01_analisis_exploratorio.ipynb`: Análisis exploratorio inicial.
   - `02_transformaciones_numpy.ipynb`: Transformaciones avanzadas con NumPy.

### Ejecutar Scripts
Los módulos en `src/` pueden ejecutarse directamente o importarse en otros scripts.

## Dataset

- **Archivo:** `data/urgencias_noprocesados_grupo08.csv`
- **Tamaño:** ~1.3 MB
- **Filas:** 4,742
- **Columnas:** 29
- **Codificación:** latin-1 (ISO-8859-1)
- **Dominio:** Salud pública - urgencias hospitalarias en Chile

## Contribuyentes

- Grupo 8 - Programación para Ciencia de Datos

## Licencia

Este proyecto es para fines educativos y de evaluación académica.