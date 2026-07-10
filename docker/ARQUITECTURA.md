[ARQUITECTURA.md](https://github.com/user-attachments/files/29872630/ARQUITECTURA.md)
# Arquitectura End-to-End del Proyecto

**Proyecto:** Análisis de Actividad Física  
**Versión:** 3.0  
**Última actualización:** Julio 2026

---

## 1. Descripción general

Este proyecto implementa una solución end-to-end para el análisis de datos de actividad física.

La solución integra:

- Pipeline ETL para extracción, limpieza, transformación y carga de datos.
- API REST desarrollada con FastAPI.
- Dashboard interactivo desarrollado con Streamlit.
- Modelos de clasificación y regresión con Scikit-learn.
- Pruebas automatizadas con Pytest.
- Containerización con Docker y Docker Compose.
- Documentación técnica y evidencias de resultados.

El notebook principal del proyecto es:

```text
notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb
```

---

## 2. Objetivos

- Limpiar datos con valores nulos, duplicados y registros inválidos.
- Validar esquemas, tipos de datos y reglas de negocio.
- Integrar múltiples fuentes de datos.
- Aplicar transformaciones avanzadas con Pandas.
- Implementar modelos supervisados de clasificación y regresión.
- Exponer datos y KPIs mediante una API REST.
- Visualizar resultados en un dashboard interactivo.
- Ejecutar los servicios mediante contenedores Docker.
- Mantener una estructura profesional y reproducible.

---

## 3. Arquitectura general

```text
┌─────────────────────────────────────────────────────────────┐
│                         USUARIO                             │
│                                                             │
│  Navegador web                                              │
│  ├── Dashboard Streamlit: http://localhost:8501             │
│  └── API FastAPI:       http://localhost:8000/docs          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DOCKER COMPOSE                         │
│                                                             │
│  ┌──────────────────────┐    ┌───────────────────────────┐  │
│  │ Dashboard            │    │ API REST                  │  │
│  │ Streamlit            │    │ FastAPI + Uvicorn         │  │
│  │ Puerto 8501          │    │ Puerto 8000               │  │
│  └──────────────────────┘    └───────────────────────────┘  │
│                │                         │                  │
│                └──────────────┬──────────┘                  │
│                               │                             │
│                        Red Docker Bridge                    │
│                        actividad_red                        │
│                               │                             │
│                               ▼                             │
│                    data/processed/                          │
│              hourlySteps_eft_final.csv                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PIPELINE ETL + ML                       │
│                                                             │
│  CSV crudos → limpieza → transformación → modelos → KPIs    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Arquitectura de contenedores

La solución utiliza un único `Dockerfile` para construir una imagen base común.

El archivo `docker-compose.yml` crea dos servicios:

| Servicio | Tecnología | Puerto | Función |
|---|---|---:|---|
| `dashboard` | Streamlit | 8501 | Visualización interactiva |
| `api` | FastAPI + Uvicorn | 8000 | Exposición de endpoints REST |

Ambos servicios acceden al dataset procesado:

```text
data/processed/hourlySteps_eft_final.csv
```

La red interna utilizada es:

```text
actividad_red
```

La carpeta `data/` puede montarse en modo de solo lectura para evitar modificaciones accidentales.

---

## 5. Pipeline ETL

```text
hourlySteps_sucio.csv
        │
        ▼
┌──────────────────────────────┐
│ EXTRACCIÓN                   │
│ - Lectura con pd.read_csv    │
│ - Validación de archivos     │
│ - Validación de columnas     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ TRANSFORMACIÓN               │
│ - Conversión de tipos        │
│ - Eliminación de duplicados  │
│ - Imputación de nulos        │
│ - Tratamiento de negativos   │
│ - Winsorización de outliers  │
│ - Variables temporales       │
│ - Vectorización              │
│ - Pivot y melt               │
│ - Joins validados            │
│ - Procesamiento por chunks   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ MACHINE LEARNING             │
│ - Clasificación              │
│ - Regresión                  │
│ - Pipelines                  │
│ - Validación cruzada         │
│ - GridSearchCV               │
│ - Métricas e importancia     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ CARGA                        │
│ - CSV procesado              │
│ - SQLite                     │
│ - KPIs JSON                  │
│ - Métricas CSV               │
│ - Modelos joblib locales     │
└──────────────┬───────────────┘
               │
               ▼
hourlySteps_eft_final.csv
```

---

## 6. Fuentes de datos

El notebook utiliza los siguientes archivos:

```text
hourlySteps_sucio.csv
hourlySteps_merged.csv
hourlySteps.csv
```

La lectura se realiza de manera explícita:

```python
df_sucio = pd.read_csv("hourlySteps_sucio.csv")
df_merged = pd.read_csv("hourlySteps_merged.csv")
df_procesado_existente = pd.read_csv("hourlySteps.csv")
```

---

## 7. Validaciones del pipeline

El pipeline valida:

- Existencia de archivos.
- Presencia de columnas requeridas.
- Dataset no vacío.
- Tipos de datos correctos.
- Valores nulos en columnas críticas.
- Duplicados por usuario y hora.
- Valores negativos en `StepTotal`.
- Rango válido de horas.
- Variable binaria `FinDeSemana`.
- Integridad de los joins.
- Existencia de artefactos exportados.

---

## 8. Transformaciones avanzadas

El notebook demuestra:

- Filtros avanzados con múltiples condiciones.
- Agrupaciones múltiples con `groupby`.
- Joins con validación `many_to_one`.
- Tablas dinámicas con `pivot_table`.
- Cambio de formato con `melt`.
- Vectorización con NumPy.
- Broadcasting para variables cíclicas.
- Procesamiento por fragmentos con `chunksize`.
- Optimización de memoria mediante tipos compactos.

---

## 9. Modelos de machine learning

### 9.1 Clasificación

Objetivo:

```text
Predecir si una hora presenta actividad alta.
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

Se aplica:

- Pipeline de Scikit-learn.
- Imputación.
- Escalado.
- Validación cruzada.
- GridSearchCV.
- Matriz de confusión.
- Importancia de variables.

### 9.2 Regresión

Objetivo:

```text
Estimar la cantidad de pasos en una hora.
```

Modelos utilizados:

- Linear Regression.
- Random Forest Regressor.

Métricas:

- MAE.
- RMSE.
- R².

---

## 10. API REST

**Ubicación:**

```text
api/api.py
```

**Tecnologías:**

- FastAPI.
- Uvicorn.
- Pandas.
- Pydantic.

**Puerto:**

```text
8000
```

### Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Estado general de la API |
| GET | `/health` | Disponibilidad y calidad del dataset |
| GET | `/kpis` | KPIs principales |
| GET | `/resumen-columnas` | Estructura y calidad de datos |
| GET | `/muestra` | Muestra configurable |
| GET | `/actividad-por-hora` | Estadísticas por hora |
| GET | `/actividad-por-dia` | Estadísticas por día |
| GET | `/usuario/{usuario_id}` | Resumen por usuario |
| GET | `/buscar` | Filtros combinados |

### Documentación automática

```text
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
```

---

## 11. Dashboard interactivo

**Ubicación:**

```text
dashboards/app_streamlit.py
```

**Tecnologías:**

- Streamlit.
- Pandas.

**Puerto:**

```text
8501
```

### Funcionalidades

- Filtro por usuario.
- Filtro por rango de horas.
- Filtro por tipo de día.
- Total de registros.
- Total de usuarios.
- Promedio de pasos.
- Hora de mayor actividad.
- Promedio de pasos por hora.
- Promedio de pasos por día.
- Comparación entre día hábil y fin de semana.
- Ranking de usuarios.
- Información de calidad.
- Descarga de datos filtrados.

---

## 12. Estructura del proyecto

```text
proyecto1/
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
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

## 13. Resultados generados

El notebook exporta:

```text
data/processed/hourlySteps_eft_final.csv
results/kpis_eft.json
results/metricas_clasificacion.csv
results/metricas_regresion.csv
results/importancia_variables.csv
```

Los modelos se generan localmente:

```text
models/clasificador_actividad.joblib
models/regresor_pasos.joblib
```

Los archivos `.joblib` pueden no almacenarse en GitHub debido a su tamaño. Se regeneran ejecutando el notebook principal.

---

## 14. Variables de entorno

Ejemplo de archivo `.env`:

```env
APP_NAME=Proyecto ETL Dashboard
ENVIRONMENT=development
RAW_DATA_PATH=./data/raw/hourlySteps_sucio.csv
PROCESSED_DATA_PATH=./data/processed/hourlySteps_eft_final.csv
API_PORT=8000
DASHBOARD_PORT=8501
```

---

## 15. Requisitos

Dependencias principales:

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

---

## 16. Ejecución con Docker

### 16.1 Clonar el repositorio

```bash
git clone https://github.com/jjuliiann/proyecto1.git
cd proyecto1
```

### 16.2 Crear archivo `.env`

En Linux o macOS:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
copy .env.example .env
```

### 16.3 Levantar servicios

Desde la raíz:

```bash
docker compose -f docker/docker-compose.yml up --build
```

También puede ejecutarse desde la carpeta `docker`:

```bash
cd docker
docker compose up --build
```

### 16.4 Acceso

```text
Dashboard: http://localhost:8501
API:       http://localhost:8000
Swagger:   http://localhost:8000/docs
```

---

## 17. Verificación del sistema

### Verificar contenedores

```bash
docker compose -f docker/docker-compose.yml ps
```

### Ver logs

```bash
docker compose -f docker/docker-compose.yml logs -f
```

### Probar API

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/kpis
curl http://localhost:8000/actividad-por-hora
```

### Ejecutar pruebas

```bash
docker compose -f docker/docker-compose.yml exec api pytest tests/ -v
```

---

## 18. Pruebas automatizadas

**Ubicación:**

```text
tests/
```

**Framework:**

```text
pytest
```

Pruebas recomendadas:

- Dataset procesado existe.
- Columnas requeridas presentes.
- Sin nulos críticos.
- Sin duplicados.
- `StepTotal` numérico.
- API responde correctamente.
- Endpoints principales retornan HTTP 200.
- Dashboard puede cargar el dataset.

---

## 19. Flujo de datos

```text
hourlySteps_sucio.csv
        │
        ▼
Notebook ETL + ML
        │
        ├── Limpieza
        ├── Transformación
        ├── Validación
        ├── Clasificación
        ├── Regresión
        └── Exportación
        │
        ▼
hourlySteps_eft_final.csv
        │
        ├── API FastAPI
        ├── Dashboard Streamlit
        ├── Resultados
        └── Pruebas
```

---

## 20. Tecnologías utilizadas

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
| Control de versiones | Git, GitHub |

---

## 21. Troubleshooting

### Error: no se encuentra el dataset

Verifique:

```text
data/processed/hourlySteps_eft_final.csv
```

Si no existe, ejecute:

```text
notebooks/06_eft_pipeline_ml_end_to_end_v3.ipynb
```

### Error: puerto ocupado

Para API:

```text
8000
```

Para dashboard:

```text
8501
```

Cambie los puertos en `.env` o en `docker-compose.yml`.

### Error de dependencias

Reconstruya sin caché:

```bash
docker compose -f docker/docker-compose.yml build --no-cache
docker compose -f docker/docker-compose.yml up
```

### Error al conectar con Docker

Compruebe que Docker Desktop esté iniciado:

```bash
docker --version
docker compose version
```

---

## 22. Detener los servicios

```bash
docker compose -f docker/docker-compose.yml down
```

Para detener sin eliminar:

```bash
docker compose -f docker/docker-compose.yml stop
```

---

## 23. Resumen de puertos

| Servicio | Puerto |
|---|---:|
| Dashboard Streamlit | 8501 |
| API FastAPI | 8000 |
| Swagger UI | 8000/docs |

---

## 24. Contribuyentes

- Vicente Castro
- Lucas Fernandez
- Julian Martinez

---

## 25. Conclusión

La arquitectura implementada permite ejecutar una solución reproducible de ciencia de datos que cubre extracción, transformación, machine learning, API, dashboard, testing y despliegue con Docker.

El diseño separa responsabilidades, facilita el mantenimiento y permite presentar una demostración end-to-end alineada con los requerimientos de la Evaluación Final Transversal.
