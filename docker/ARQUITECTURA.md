# 🏗️ Arquitectura End-to-End del Proyecto

**Proyecto:** Análisis de Actividad Física  
**Versión:** 2.0  
**Última actualización:** Junio 2026

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura de Contenedores](#arquitectura-de-contenedores)
3. [Pipeline ETL](#pipeline-etl)
4. [Componentes Principales](#componentes-principales)
5. [Flujo de Datos](#flujo-de-datos)
6. [Tecnologías Utilizadas](#tecnologías-utilizadas)
7. [Instrucciones de Instalación](#instrucciones-de-instalación)
8. [Verificación del Sistema](#verificación-del-sistema)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Descripción General

Este proyecto es una **solución end-to-end** para el análisis de datos de actividad física. Integra:

- **Extracción y Limpieza de Datos (ETL)**: Procesa datos crudos en formato CSV
- **API REST**: Expone KPIs y datos procesados mediante FastAPI
- **Dashboard Interactivo**: Visualización en tiempo real con Streamlit
- **Pruebas Automatizadas**: Validación de calidad de datos
- **Containerización**: Despliegue reproducible con Docker

### 🎯 Objetivos

✅ Limpiar dataset con valores nulos y duplicados  
✅ Transformar datos mediante pipeline ETL  
✅ Generar nuevas variables (feature engineering)  
✅ Exponer resultados vía API REST  
✅ Visualizar insights en dashboard interactivo  
✅ Ejecutar todo en contenedores Docker

---

## 🐳 Arquitectura de Contenedores

```
┌─────────────────────────────────────────────────────────────┐
│                      HOST (Tu Computador)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Docker Engine (Docker Desktop)               │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │                                                       │  │
│  │  ┌─────────────────┐  ┌──────────────────────────┐  │  │
│  │  │  dashboard      │  │        api               │  │  │
│  │  │  (Streamlit)    │  │      (FastAPI)           │  │  │
│  │  │  Puerto 8501    │  │      Puerto 8000         │  │  │
│  │  │  Imagen: app    │  │      Imagen: app         │  │  │
│  │  └─────────────────┘  └──────────────────────────┘  │  │
│  │           │                       │                  │  │
│  │           └───────────┬───────────┘                  │  │
│  │                       │                              │  │
│  │                 Red bridge: actividad_red            │  │
│  │                 (172.20.0.0/16)                      │  │
│  │                       │                              │  │
│  │           ┌───────────┴───────────┐                 │  │
│  │           │                       │                 │  │
│  │      Volumen: data/               │                 │  │
│  │      (Persistencia de datos)       │                 │  │
│  │      Modo: read-only               │                 │  │
│  │                                    │                 │  │
│  │    Variables de entorno           │                 │  │
│  │    (.env)                         │                 │  │
│  │                                    │                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Acceso desde navegador                     │
├─────────────────────────────────────────────────────────────┤
│  Dashboard: http://localhost:8501                            │
│  API Docs:  http://localhost:8000/docs                       │
│  API Root:  http://localhost:8000/                           │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Componentes de la Arquitectura

| Componente | Tecnología | Puerto | Función |
|-----------|-----------|--------|---------|
| **dashboard** | Streamlit | 8501 | Visualización interactiva de datos |
| **api** | FastAPI + Uvicorn | 8000 | API REST con endpoints de datos |
| **Red** | Docker Bridge | - | Comunicación entre contenedores |
| **Volumen** | Docker Volume | - | Persistencia de datos CSV |
| **Imagen** | Python 3.11-slim | - | Sistema operativo base |

---

## 📦 Pipeline ETL

```
┌──────────────────┐
│   Raw Dataset    │
│   (sucio.csv)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      EXTRACCIÓN (Extract)            │
│  • Leer CSV                          │
│  • Validar estructura                │
│  • Verificar columnas                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      TRANSFORMACIÓN (Transform)      │
│  • Eliminar duplicados               │
│  • Completar valores nulos           │
│  • Convertir tipos de datos          │
│  • Feature engineering:              │
│    - Hora del día                    │
│    - Día de la semana                │
│    - Fin de semana (bool)            │
│  • Normalizar datos                  │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      CARGA (Load)                    │
│  • Guardar CSV procesado             │
│  • Crear base de datos (SQLite)      │
│  • Validar integridad                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│   Processed Dataset (limpio)         │
│   Listo para análisis                │
└──────────────────────────────────────┘
```

### 📋 Validaciones del Pipeline

- ✅ Dataset existe
- ✅ Columnas requeridas presentes
- ✅ Sin valores nulos (NaN)
- ✅ Sin duplicados
- ✅ Tipos de datos correctos (numéricos para StepTotal)
- ✅ Rango de datos válido

---

## 🔧 Componentes Principales

### 1️⃣ Dashboard (Streamlit)

**Ubicación:** `dashboards/app_streamlit.py`  
**Puerto:** 8501  
**Tecnología:** Streamlit, Plotly, Pandas

#### Vistas disponibles:

- **📊 Ejecutiva**: KPIs principales
  - Total de registros
  - Promedio de pasos
  - Máximo de pasos
  - Histograma de distribución

- **🔧 Técnica**: Calidad de datos
  - Columnas y tipos
  - Valores nulos
  - Registros duplicados
  - Estadísticas descriptivas

- **📈 Operativa**: Análisis temporal
  - Pasos por hora del día
  - Pasos por día de semana
  - Comparación semana vs fin de semana
  - Tendencias

#### Acceso:
```bash
http://localhost:8501
```

---

### 2️⃣ API REST (FastAPI)

**Ubicación:** `api/api.py`  
**Puerto:** 8000  
**Tecnología:** FastAPI, Uvicorn, Pydantic

#### Endpoints disponibles:

| Método | Endpoint | Descripción | Respuesta |
|--------|----------|-------------|-----------|
| GET | `/` | Health check | `{"status": "OK"}` |
| GET | `/kpis` | KPIs principales | Total, promedio, máx, mín pasos |
| GET | `/resumen-columnas` | Calidad de datos | Columnas, nulos, duplicados |
| GET | `/muestra` | Primeros 10 registros | Muestra de datos procesados |

#### Documentación interactiva:
```bash
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
```

---

### 3️⃣ Datos

**Estructura de carpetas:**

```
data/
├── raw/                           # Datos crudos
│   └── hourlySteps_sucio.csv      # Dataset sin procesar
├── og/                            # Datos originales
│   └── hourlySteps_merged.csv     # Dataset consolidado
└── processed/                      # Datos procesados
    └── hourlySteps.csv            # Dataset limpio (producción)
```

**Características:**

- **raw/hourlySteps_sucio.csv**: Dataset original con problemas
  - 30,000 registros (aprox)
  - ~20% valores nulos artificiales
  - ~15% duplicados artificiales

- **processed/hourlySteps.csv**: Dataset transformado
  - Valores nulos eliminados
  - Duplicados eliminados
  - Variables nuevas creadas
  - Listo para análisis

---

### 4️⃣ Pruebas Automatizadas

**Ubicación:** `tests/`  
**Framework:** Pytest

#### Pruebas incluidas:

```python
✅ test_dataset_exists()           # Dataset procesado existe
✅ test_required_columns()          # Columnas necesarias presentes
✅ test_no_nulls()                  # Sin valores nulos
✅ test_no_duplicates()             # Sin duplicados
✅ test_stepstotal_numeric()        # Columna StepTotal es numérica
```

#### Ejecutar tests:
```bash
docker compose exec api pytest tests/ -v
```

---

## 🔄 Flujo de Datos

```
ENTRADA                    PROCESAMIENTO                 SALIDA
═════════════════════════════════════════════════════════════════════

hourlySteps_sucio.csv  ──►  ETL Pipeline  ──►  hourlySteps.csv
(crudo, con errores)       (limpieza,           (procesado,
                           transformación)       listo para uso)

                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
           API REST       Dashboard        Pruebas
           (FastAPI)      (Streamlit)      (Pytest)
           
             │              │               │
             └──────────────┬───────────────┘
                            │
                    Usuarios / Stakeholders
                    
                    • Ejecutivos (KPIs)
                    • Técnicos (Calidad)
                    • Operativos (Análisis)
```

---

## 🛠️ Tecnologías Utilizadas

### Lenguaje y Runtime
- **Python 3.11** (slim): Ligero, eficiente

### Data Processing
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Cálculos numéricos
- **Scikit-learn**: Pipeline ETL, normalización

### Visualización
- **Streamlit**: Dashboard interactivo
- **Plotly**: Gráficos interactivos
- **Matplotlib**: Gráficos estáticos

### API y Backend
- **FastAPI**: Framework web moderno
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validación de datos

### Testing
- **Pytest**: Framework de pruebas
- **Python-dotenv**: Gestión de variables de entorno

### Containerización
- **Docker**: Containerización
- **Docker Compose**: Orquestación de servicios

---

## 🚀 Instrucciones de Instalación

### Requisitos Previos

```bash
# 1. Git
git --version              # Verificar instalación

# 2. Docker Desktop
docker --version           # Verificar Docker
docker compose version     # Verificar Docker Compose
```

### Paso a Paso

#### 1. Clonar el repositorio

```bash
git clone https://github.com/jjuliiann/proyecto1.git
cd proyecto1
```

#### 2. Configurar variables de entorno

```bash
# Copiar plantilla a .env (Linux/Mac)
cp .env.example .env

# O en Windows PowerShell:
copy .env.example .env

# Verificar que se creó correctamente
cat .env  # Linux/Mac
type .env # Windows
```

**Contenido esperado de .env:**
```
APP_NAME=Proyecto ETL Dashboard
ENVIRONMENT=development
RAW_DATA_PATH=./data/raw/hourlySteps_sucio.csv
PROCESSED_DATA_PATH=./data/processed/hourlySteps.csv
API_PORT=8000
DASHBOARD_PORT=8501
```

#### 3. Asegurar que los datos existan

```bash
# Verificar que existen los archivos de datos
ls data/raw/hourlySteps_sucio.csv           # Debe existir
ls data/og/hourlySteps_merged.csv           # Debe existir
ls data/processed/hourlySteps.csv           # Será creado por ETL
```

#### 4. Levantar los servicios Docker

```bash
# Entrar a la carpeta docker
cd docker

# Construir e iniciar servicios
# Primera vez: 2-5 minutos (descarga imágenes, instala dependencias)
docker compose up --build

# Posteriores: más rápido (reutiliza capas)
docker compose up
```

**Salida esperada:**
```
dashboard_actividad_fisica  | You can now view your Streamlit app in your browser.
dashboard_actividad_fisica  | Local URL: http://localhost:8501
api_actividad_fisica        | Uvicorn running on http://0.0.0.0:8000
```

#### 5. Verificar servicios (terminal nueva)

```bash
# En otra terminal, dentro de carpeta docker
cd docker
docker compose ps

# Salida esperada:
# NAME                          STATUS
# dashboard_actividad_fisica    Up (healthy)
# api_actividad_fisica          Up (healthy)
```

---

## ✅ Verificación del Sistema

### 1. Verificar Dashboard

```bash
# Abrir navegador:
# http://localhost:8501

# Debe mostrar:
# - Sidebar con "Menú de audiencia"
# - Opciones: Ejecutiva, Técnica, Operativa
# - Filtro de día
# - Gráficos interactivos
```

### 2. Verificar API

```bash
# Opción A: Swagger UI (recomendado)
# http://localhost:8000/docs

# Opción B: Desde terminal
curl http://localhost:8000/

# Respuesta esperada:
# {"status":"OK","message":"API de Actividad Física"}

# Probar endpoints
curl http://localhost:8000/kpis
curl http://localhost:8000/resumen-columnas
curl http://localhost:8000/muestra
```

### 3. Ejecutar Pruebas

```bash
# Terminal en carpeta docker
cd docker

# Opción A: Ejecutar tests
docker compose exec api pytest tests/ -v

# Salida esperada:
# tests/test_etl.py::test_dataset_exists PASSED
# tests/test_etl.py::test_required_columns PASSED
# tests/test_etl.py::test_no_nulls PASSED
# tests/test_etl.py::test_no_duplicates PASSED
# tests/test_etl.py::test_stepstotal_numeric PASSED
# ===== 5 passed in 0.42s =====

# Opción B: Ejecutar con servicio tests
docker compose run --rm tests
```

### 4. Ver Logs

```bash
# Logs en tiempo real
docker compose logs -f

# Solo dashboard
docker compose logs -f dashboard

# Solo API
docker compose logs -f api

# Últimas 100 líneas
docker compose logs --tail=100
```

---

## 🐛 Troubleshooting

### ❌ Error: "command not found: docker"

**Solución:** Docker no está instalado o no está en PATH
```bash
# Descargar e instalar desde:
# https://www.docker.com/products/docker-desktop

# Reiniciar terminal después de instalar
```

---

### ❌ Error: "Cannot connect to Docker daemon"

**Solución:** Docker Desktop no está corriendo

```bash
# En Windows/Mac:
# Abre Docker Desktop manualmente

# En Linux:
sudo systemctl start docker

# Verificar que funciona:
docker --version
```

---

### ❌ Error: "Port 8501 is already in use"

**Solución:** Otro proceso está usando el puerto

```bash
# Encontrar qué proceso usa el puerto
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# Matar proceso o usar puerto diferente
# Opción A: Cambiar puerto en .env
DASHBOARD_PORT=8502

# Opción B: Matar proceso
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

---

### ❌ Error: "ModuleNotFoundError: No module named 'pandas'"

**Solución:** Dependencias no instaladas correctamente

```bash
cd docker

# Reconstruir imagen sin caché
docker compose build --no-cache

# Levantar nuevamente
docker compose up
```

---

### ❌ Error: "FileNotFoundError: data/processed/hourlySteps.csv"

**Solución:** El archivo de datos no existe o no fue procesado

```bash
# Verificar que archivo existe
ls data/processed/hourlySteps.csv

# Si no existe, ejecutar ETL manualmente
# (El notebook `notebooks/etl.ipynb` genera este archivo)

# O copiar desde datos originales
cp data/raw/hourlySteps_sucio.csv data/processed/hourlySteps.csv
```

---

### ❌ Health check fails: "timeout"

**Solución:** Servicios están lentos al iniciar

```bash
# Esperar 20-30 segundos y verificar estado
docker compose ps

# Ver logs para ver qué ocurre
docker compose logs -f dashboard
docker compose logs -f api

# Si sigue fallando, reconstruir
docker compose down
docker compose up --build
```

---

## 🛑 Detener los Servicios

### Opción A: Desde la terminal donde corre docker compose

```bash
# Presionar Ctrl + C
Ctrl + C
```

### Opción B: Desde otra terminal

```bash
cd docker

# Detener y eliminar contenedores
docker compose down

# Solo detener (mantener contenedores)
docker compose stop

# Reanudar contenedores
docker compose start
```

---

## 📊 Resumen de Comandos Rápidos

```bash
# ═════════════════════════════════════════════════════════════
# INSTALACIÓN Y CONFIGURACIÓN
# ═════════════════════════════════════════════════════════════

git clone https://github.com/jjuliiann/proyecto1.git
cd proyecto1
cp .env.example .env
cd docker

# ═════════════════════════════════════════════════════════════
# EJECUTAR SERVICIOS
# ═════════════════════════════════════════════════════════════

docker compose up --build              # Primera vez (lento)
docker compose up                      # Posteriores (rápido)
docker compose ps                      # Ver estado
docker compose logs -f                 # Ver logs en tiempo real
docker compose down                    # Detener servicios

# ═════════════════════════════════════════════════════════════
# ACCEDER A SERVICIOS
# ═════════════════════════════════════════════════════════════

# Dashboard:       http://localhost:8501
# API Docs:        http://localhost:8000/docs
# API Root:        http://localhost:8000/

# ═════════════════════════════════════════════════════════════
# PRUEBAS Y VERIFICACIÓN
# ═════════════════════════════════════════════════════════════

docker compose exec api pytest tests/ -v
docker compose run --rm tests
curl http://localhost:8000/

# ═════════════════════════════════════════════════════════════
# DESARROLLO
# ═════════════════════════════════════════════════════════════

docker compose up dashboard            # Solo dashboard
docker compose up api                  # Solo API
docker compose restart api             # Reiniciar servicio
docker compose rm tests                # Eliminar contenedor tests
```

---

## 📚 Información Adicional

### Archivos Clave

- **`docker/Dockerfile`**: Definición de imagen (multi-stage, optimizado)
- **`docker/docker-compose.yml`**: Orquestación de servicios
- **`docker/.dockerignore`**: Archivos excluidos de imagen
- **`.env.example`**: Plantilla de variables de entorno
- **`requirements.txt`**: Dependencias Python

### Contribuyentes

- **Vicente Castro**
- **Lucas Fernandez**
- **Julian Martinez**

### Licencia

MIT License (o la licencia que uses)

---

## 🎓 Resumen de la Arquitectura

| Aspecto | Detalle |
|--------|--------|
| **Lenguaje** | Python 3.11 |
| **Containerización** | Docker + Docker Compose |
| **API** | FastAPI (8000) |
| **Dashboard** | Streamlit (8501) |
| **Base de Datos** | CSV + SQLite (opcional) |
| **Testing** | Pytest |
| **Red** | Bridge (172.20.0.0/16) |
| **Volúmenes** | Data (read-only) |
| **Health Checks** | Habilitados |
| **Logging** | JSON-file (10MB/3 archivos) |
| **Seguridad** | Usuario no-root en imagen |

---

**¡Listo para usar! 🎉**
