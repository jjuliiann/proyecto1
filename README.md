[README.md](https://github.com/user-attachments/files/29873293/README.md)
# Proyecto End-to-End de Análisis de Actividad Física

## Evaluación Final Transversal — Programación para la Ciencia de Datos

Este repositorio contiene una solución completa de ciencia de datos aplicada al análisis de actividad física a partir de registros horarios de pasos.

El proyecto integra:

- Pipeline ETL.
- Limpieza y transformación de datos.
- Análisis exploratorio.
- Modelos de clasificación y regresión.
- API REST con FastAPI.
- Dashboard interactivo con Streamlit.
- Pruebas automatizadas con Pytest.
- Containerización con Docker.
- Integración continua con GitHub Actions.
- Documentación técnica y evidencias de resultados.

---

## Integrantes

- Vicente Castro
- Lucas Fernandez
- Julian Martinez

---

## Objetivo del proyecto

El objetivo es transformar datos crudos de actividad física en información útil para análisis y toma de decisiones.

La solución permite:

- detectar registros inválidos;
- limpiar valores nulos y duplicados;
- generar variables temporales;
- analizar patrones de actividad;
- predecir períodos de actividad alta;
- estimar la cantidad de pasos por hora;
- consultar KPIs desde una API;
- visualizar resultados mediante un dashboard;
- validar automáticamente la calidad de los datos.

---

## Notebook principal

El notebook principal de la Evaluación Final Transversal se encuentra en:

```text
notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb
```

Este cuaderno incluye:

- lectura de múltiples archivos CSV;
- validación de esquemas;
- diagnóstico de calidad;
- limpieza de valores nulos;
- eliminación de duplicados;
- tratamiento de valores negativos;
- winsorización de outliers;
- filtros avanzados;
- agrupaciones múltiples;
- joins con validación de cardinalidad;
- transformaciones con `pivot_table` y `melt`;
- vectorización y broadcasting;
- lectura por chunks;
- integración con SQLite;
- clasificación con Scikit-learn;
- regresión con Scikit-learn;
- pipelines;
- validación cruzada;
- optimización con `GridSearchCV`;
- métricas de evaluación;
- importancia de variables;
- exportación de KPIs, resultados y modelos.

---

## Archivos de datos

Los archivos principales utilizados son:

```text
hourlySteps_sucio.csv
hourlySteps_merged.csv
hourlySteps.csv
```

La lectura en el notebook se realiza de forma explícita:

```python
df_sucio = pd.read_csv("hourlySteps_sucio.csv")
df_merged = pd.read_csv("hourlySteps_merged.csv")
df_procesado_existente = pd.read_csv("hourlySteps.csv")
```

El dataset final generado por el pipeline es:

```text
data/processed/hourlySteps_eft_final.csv
```

---

## Estructura del repositorio

```text
proyecto1/
├── .github/
│   └── workflows/
│       └── tests.yml
├── api/
│   └── api.py
├── dashboards/
│   └── app_streamlit.py
├── data/
│   ├── raw/
│   │   └── hourlySteps_sucio.csv
│   ├── og/
│   │   └── hourlySteps_merged.csv
│   └── processed/
│       ├── hourlySteps.csv
│       └── hourlySteps_eft_final.csv
├── docker/
│   ├── ARQUITECTURA.md
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
├── models/
│   └── .gitkeep
├── notebooks/
│   └── 06_eft_pipeline_ml_end_to_end_v3.ipynb
├── results/
│   ├── importancia_variables.csv
│   ├── kpis_eft.json
│   ├── metricas_clasificacion.csv
│   └── metricas_regresion.csv
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   └── hyperparameter_tuning.py
├── tests/
│   └── test_etl.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Pipeline ETL

### Extract

Se cargan las fuentes mediante Pandas:

```python
pd.read_csv()
```

Durante la extracción se valida:

- existencia del archivo;
- estructura del dataset;
- columnas requeridas;
- cantidad de registros;
- memoria utilizada;
- tipos de datos.

### Transform

Se aplican las siguientes operaciones:

- conversión de tipos;
- eliminación de duplicados;
- imputación contextual;
- tratamiento de valores negativos;
- tratamiento de outliers;
- creación de variables temporales;
- codificación cíclica;
- filtros avanzados;
- agrupaciones múltiples;
- joins validados;
- pivot;
- melt;
- vectorización;
- broadcasting;
- procesamiento por chunks.

### Load

Los resultados se almacenan en:

```text
data/processed/hourlySteps_eft_final.csv
```

También se generan:

```text
results/kpis_eft.json
results/metricas_clasificacion.csv
results/metricas_regresion.csv
results/importancia_variables.csv
```

Además, el notebook crea una base SQLite para consultas agregadas.

---

## Modelos de machine learning

### Clasificación

Objetivo:

```text
Predecir si una hora corresponde a actividad alta.
```

Modelos utilizados:

- Logistic Regression.
- Random Forest Classifier.

Métricas:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- ROC-AUC.
- Matriz de confusión.

### Regresión

Objetivo:

```text
Estimar la cantidad de pasos de una hora.
```

Modelos utilizados:

- Linear Regression.
- Random Forest Regressor.

Métricas:

- MAE.
- RMSE.
- R².

### Optimización

Se utiliza:

- Pipeline de Scikit-learn.
- Imputación.
- Estandarización.
- Validación cruzada.
- GridSearchCV.
- Selección del mejor modelo.
- Importancia de variables.

---

## Modelos entrenados

Los modelos se generan automáticamente al ejecutar:

```text
notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb
```

Los artefactos generados localmente son:

```text
models/clasificador_actividad.joblib
models/regresor_pasos.joblib
```

Estos archivos no se almacenan en GitHub debido a su tamaño.

La carpeta `models/` conserva su estructura mediante:

```text
models/.gitkeep
```

Los modelos pueden regenerarse ejecutando el notebook principal.

---

## API REST

La API se encuentra en:

```text
api/api.py
```

Tecnologías:

- FastAPI.
- Uvicorn.
- Pandas.

Puerto:

```text
8000
```

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Estado general de la API |
| GET | `/health` | Estado y calidad del dataset |
| GET | `/kpis` | KPIs principales |
| GET | `/resumen-columnas` | Información de columnas y calidad |
| GET | `/muestra` | Muestra configurable |
| GET | `/actividad-por-hora` | Estadísticas por hora |
| GET | `/actividad-por-dia` | Estadísticas por día |
| GET | `/usuario/{usuario_id}` | Resumen individual |
| GET | `/buscar` | Filtros combinados |

Documentación automática:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

---

## Dashboard Streamlit

El dashboard se encuentra en:

```text
dashboards/app_streamlit.py
```

Puerto:

```text
8501
```

Funciones principales:

- filtro por usuario;
- filtro por rango horario;
- filtro por tipo de día;
- total de registros;
- total de usuarios;
- promedio de pasos;
- hora más activa;
- gráfico de actividad por hora;
- gráfico de actividad por día;
- comparación entre días hábiles y fines de semana;
- ranking de usuarios;
- detalle de calidad;
- descarga de datos filtrados.

Acceso:

```text
http://localhost:8501
```

---

## Pruebas automatizadas

Las pruebas se encuentran en:

```text
tests/test_etl.py
```

Se valida:

- existencia del dataset;
- dataset no vacío;
- columnas requeridas;
- ausencia de nulos críticos;
- ausencia de duplicados por usuario y hora;
- tipo numérico de `StepTotal`;
- ausencia de pasos negativos;
- rango válido de horas;
- variable `FinDeSemana` binaria.

Ejecutar localmente:

```bash
pytest tests/ -v
```

Resultado esperado:

```text
9 passed
```

---

## Integración continua

El workflow se encuentra en:

```text
.github/workflows/tests.yml
```

GitHub Actions ejecuta automáticamente las pruebas cuando:

- se realiza un push a `main`;
- se abre un pull request hacia `main`;
- se inicia manualmente el workflow.

El workflow:

1. descarga el repositorio;
2. verifica el dataset final;
3. configura Python 3.11;
4. instala dependencias;
5. ejecuta Pytest.

Estado esperado:

```text
Check verde
```

---

## Docker

La configuración se encuentra en:

```text
docker/
```

Archivos:

```text
docker/Dockerfile
docker/docker-compose.yml
docker/ARQUITECTURA.md
```

Servicios:

| Servicio | Tecnología | Puerto |
|---|---|---:|
| Dashboard | Streamlit | 8501 |
| API | FastAPI | 8000 |

### Ejecutar con Docker

Desde la raíz:

```bash
docker compose -f docker/docker-compose.yml up --build
```

También puede ejecutarse desde la carpeta `docker`:

```bash
cd docker
docker compose up --build
```

Accesos:

```text
Dashboard: http://localhost:8501
API:       http://localhost:8000
Swagger:   http://localhost:8000/docs
```

Detener servicios:

```bash
docker compose -f docker/docker-compose.yml down
```

---

## Variables de entorno

Ejemplo de `.env`:

```env
APP_NAME=Proyecto ETL Dashboard
ENVIRONMENT=development
RAW_DATA_PATH=./data/raw/hourlySteps_sucio.csv
PROCESSED_DATA_PATH=./data/processed/hourlySteps_eft_final.csv
API_PORT=8000
DASHBOARD_PORT=8501
```

---

## Dependencias

Las dependencias se encuentran en:

```text
requirements.txt
```

Principales librerías:

```text
pandas
numpy
scikit-learn
matplotlib
joblib
fastapi
uvicorn
streamlit
pytest
python-dotenv
```

Instalación:

```bash
pip install -r requirements.txt
```

---

## Ejecución en Google Colab

1. Abrir:

```text
notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb
```

2. Subir:

```text
hourlySteps_sucio.csv
hourlySteps_merged.csv
hourlySteps.csv
```

3. Seleccionar:

```text
Entorno de ejecución → Ejecutar todas
```

4. Verificar que no existan celdas con error.

5. Confirmar que las validaciones finales estén en `True`.

6. Descargar los resultados generados.

---

## Ejecución local

Clonar el repositorio:

```bash
git clone https://github.com/jjuliiann/proyecto1.git
cd proyecto1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar API:

```bash
uvicorn api.api:app --host 0.0.0.0 --port 8000
```

Ejecutar dashboard:

```bash
streamlit run dashboards/app_streamlit.py
```

Ejecutar pruebas:

```bash
pytest tests/ -v
```

---

## Resultados

Los resultados del proyecto se encuentran en:

```text
results/
```

Archivos:

```text
kpis_eft.json
metricas_clasificacion.csv
metricas_regresion.csv
importancia_variables.csv
```

Estos archivos permiten:

- comparar modelos;
- revisar métricas;
- analizar variables relevantes;
- alimentar el dashboard;
- apoyar la presentación final.

---

## Tecnologías utilizadas

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Procesamiento | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualización | Streamlit, Matplotlib |
| API | FastAPI, Uvicorn |
| Base de datos | SQLite |
| Testing | Pytest |
| Containerización | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Control de versiones | Git y GitHub |

---

## Valor de negocio

La solución permite:

- identificar horarios de mayor actividad;
- detectar períodos de baja actividad;
- apoyar campañas de bienestar;
- personalizar recomendaciones;
- generar KPIs ejecutivos;
- disponer de consultas mediante API;
- facilitar la exploración con un dashboard;
- automatizar controles de calidad.

---

## Limitaciones

- El dataset representa una población y un período específicos.
- El umbral de actividad alta es estadístico.
- La importancia de variables no demuestra causalidad.
- Para producción se requiere autenticación, monitoreo y pruebas de carga.
- Los modelos deben monitorearse ante cambios en los datos.

---

## Documentación adicional

La documentación técnica de arquitectura se encuentra en:

```text
docker/ARQUITECTURA.md
```

---

## Repositorio

```text
https://github.com/jjuliiann/proyecto1
```

---

## Conclusión

Este proyecto implementa una solución completa y reproducible de ciencia de datos.

La arquitectura integra procesamiento de datos, machine learning, API, dashboard, pruebas, Docker y CI/CD, permitiendo demostrar el funcionamiento end-to-end y el valor generado a partir de los datos de actividad física.
