

---

# Proyecto de Ciencia de Datos

## Limpieza y Transformación de Datos de Actividad Física

---

## Integrantes

Vicente Castro

Julian Martínez

Lucas Fernandez

---

## Descripción del Proyecto

El presente proyecto tiene como objetivo transformar un dataset en estado "crudo" en un conjunto de datos limpio, estructurado y listo para su análisis.

Se aplicaron técnicas fundamentales de ciencia de datos, incluyendo limpieza, transformación mediante pipelines y generación de nuevas variables (feature engineering).

---

## Dataset

* **Tipo de datos:** Actividad física (cantidad de pasos por hora)
* **Formato:** CSV
* **Origen:** Dataset obtenido de plataformas abiertas como Kaggle

### Modificación del Dataset

El dataset original se encontraba en condiciones limpias, por lo que se decidió introducir artificialmente:

* Valores nulos
* Registros duplicados

**Justificación:**
Esto permitió simular un escenario real de trabajo en ciencia de datos, donde los datos suelen presentar inconsistencias.

---

## Objetivos

* Limpiar el dataset eliminando errores e inconsistencias
* Transformar los datos utilizando herramientas automatizadas
* Generar nuevas variables relevantes
* Obtener un dataset final listo para análisis o modelamiento

---

## Metodología

El desarrollo del proyecto se estructuró en las siguientes etapas:

### 1. Diagnóstico Inicial

Se realizó un análisis exploratorio para identificar problemas en los datos:

* Detección de valores nulos
* Identificación de duplicados
* Revisión de tipos de datos

---

### 2. Limpieza de Datos

#### Eliminación de duplicados

Se utilizó la función `drop_duplicates()` para eliminar registros repetidos.

**Justificación:**
Los duplicados pueden generar sesgos en el análisis y afectar los resultados.

---

#### Eliminación de valores nulos

Se aplicó `dropna()` para eliminar filas con datos faltantes.

**Justificación técnica:**
El tamaño del dataset permitió eliminar registros sin afectar su representatividad.

---

### 3. Feature Engineering (Ingeniería de Variables)

Se crearon nuevas variables a partir de la columna temporal:

* **Hora:** permite analizar patrones diarios
* **Día:** permite analizar comportamiento semanal
* **FinDeSemana:** variable binaria para identificar fines de semana

**Justificación:**
Estas variables enriquecen el dataset y permiten detectar patrones más complejos.

---

### 4. Transformación de Datos (Pipeline)

Se implementó un pipeline utilizando `scikit-learn`, que incluye:

* `SimpleImputer` (imputación de valores faltantes)
* `StandardScaler` (normalización de datos)

**Justificación técnica:**

* Automatiza el proceso de transformación
* Asegura reproducibilidad
* Sigue buenas prácticas de la industria

---

### 5. Visualización

Se generaron gráficos para analizar el comportamiento de los datos:

* Promedio de pasos por hora
* Promedio de pasos por día

**Justificación:**
Las visualizaciones permiten identificar patrones que no son evidentes mediante estadísticas descriptivas.

---

## Resultados

### Antes

* Dataset con valores nulos y duplicados
* Variables limitadas

### Después

* Dataset limpio y consistente
* Nuevas variables creadas
* Datos escalados
* Listo para análisis o machine learning

---

## Tecnologías Utilizadas

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Google Colab

---

## Justificación del Entorno

Se utilizó **Google Colab** como entorno de desarrollo debido a:

* No requiere instalación local
* Permite trabajar en la nube
* Facilita la colaboración
* Integración directa con GitHub

---

## Estructura del Proyecto

```
data/
 |-- raw/
 |   `-- hourlySteps_sucio.csv
 |-- processed/
 |   `-- hourlySteps_clean.csv

README.md
informe_tecnico_defi.docx
proyecto_cd_final.ipynb
```

---

## Reproducibilidad

El proyecto está diseñado para ser completamente reproducible:

1. Clonar el repositorio
2. Abrir el notebook en Google Colab
3. Ejecutar todas las celdas

---

## Conclusión

Se logró transformar un dataset en estado crudo en uno limpio y estructurado, aplicando técnicas fundamentales de ciencia de datos.

El proceso desarrollado sigue un flujo real de trabajo en la industria, asegurando calidad, reproducibilidad y valor analítico en los datos.

---

# Machine Learning Project - Physical Activity Classification

## Descripción
Proyecto de Machine Learning orientado a clasificar niveles de actividad física utilizando registros horarios de pasos.

## Dataset
hourlySteps_clean.csv

## Estructura
- Exploratory Data Analysis
- Supervised Modeling
- Model Evaluation
- Hyperparameter Optimization
- Final Analysis

## Tecnologías
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

## Modelos Implementados
- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- KNN

## Optimización
- GridSearchCV
- RandomizedSearchCV

# Evaluación Parcial 3 - Solución End-to-End

## Descripción

Este proyecto desarrolla una solución end-to-end para análisis de actividad física. Integra múltiples fuentes de datos, ejecuta un pipeline ETL automatizado, presenta resultados mediante un dashboard interactivo y documenta prácticas profesionales de Git y Docker.

## Fuentes de datos

1. `data/raw/hourlySteps_sucio.csv`: dataset sucio utilizado para limpieza y transformación.
2. `data/og/hourlySteps_merged.csv`: dataset original consolidado.
3. `data/processed/hourlySteps.csv`: dataset limpio utilizado por dashboard, API y tests.

## Estructura del proyecto

```text
data/
├── raw/
├── og/
└── processed/

notebooks/      Notebooks del proyecto
src/            Scripts auxiliares
dashboards/     Dashboard interactivo
api/            API REST
docker/         Dockerfile y docker-compose
tests/          Pruebas automatizadas
docs/           Documentación técnica
```

## Pipeline ETL

El pipeline realiza:

- Extracción de datos desde CSV.
- Validación de columnas y tipos.
- Limpieza de valores nulos.
- Eliminación de duplicados.
- Transformación de fechas.
- Creación de variables como hora, día y fin de semana.
- Carga de datos procesados.

## Dashboard

El dashboard fue desarrollado con Streamlit y contiene tres vistas:

- Ejecutiva: KPIs principales.
- Técnica: calidad de datos y estructura.
- Operativa: análisis por hora y tipo de día.

## API REST

La API fue creada con FastAPI y permite consultar:

- Estado del servicio.
- KPIs principales.
- Resumen de columnas.
- Muestra de datos.

## Docker

El proyecto incluye Dockerfile y docker-compose para ejecutar dashboard y API de forma reproducible.

## Testing

Las pruebas automatizadas verifican:

- Existencia del dataset procesado.
- Columnas requeridas.
- Ausencia de nulos.
- Tipo numérico de `StepTotal`.
- Ausencia de duplicados.

## Ejecución rápida

```bash
pip install -r requirements.txt
streamlit run dashboards/app_streamlit.py
uvicorn api.api:app --reload
pytest tests/
```

## Integrantes

- Vicente Castro
- Lucas Fernandez
- Julian Martinez

## Modelos entrenados

Los modelos de clasificación y regresión se generan al ejecutar el notebook:

`notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb`

Los archivos `.joblib` no se almacenan en el repositorio debido a su tamaño.  
Las métricas, KPIs e importancia de variables se encuentran en la carpeta `results/`.

---

# Evaluación Final Transversal — Solución End-to-End

## Notebook principal

El pipeline completo de la Evaluación Final Transversal se encuentra en:

`notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb`

Este notebook implementa:

- Integración de múltiples fuentes CSV.
- Validación de esquemas y manejo de errores.
- Limpieza de valores nulos, duplicados y registros inválidos.
- Filtros avanzados y agrupaciones múltiples.
- Joins con validación de cardinalidad.
- Transformaciones con pivot, melt y vectorización.
- Procesamiento por chunks para grandes volúmenes.
- Integración con SQLite.
- Modelos de clasificación y regresión.
- Pipelines de Scikit-learn.
- Validación cruzada y optimización de hiperparámetros.
- Interpretación de métricas y variables.
- Exportación de KPIs y resultados.

## Archivos utilizados

```text
hourlySteps_sucio.csv
hourlySteps_merged.csv
hourlySteps.csv
