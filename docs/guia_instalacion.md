# Guía de Instalación y Configuración

## Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.11
- Google Colab
- GitHub
- Docker
- Librerías indicadas en `requirements.txt`

## Ejecución del notebook en Colab

1. Abrir el notebook ETL ubicado en `notebooks/`.
2. Subir al entorno de Colab la carpeta `data` con esta estructura:

```text
data/
├── raw/
│   └── hourlySteps_sucio.csv
├── og/
│   └── hourlySteps_merged.csv
└── processed/
    └── hourlySteps.csv
```

3. Verificar que las rutas del notebook sean:

```python
pd.read_csv("/content/data/raw/hourlySteps_sucio.csv")
pd.read_csv("/content/data/og/hourlySteps_merged.csv")
pd.read_csv("/content/data/processed/hourlySteps.csv")
```

4. Ejecutar las celdas en orden.
5. Revisar que se generen las validaciones, transformaciones y visualizaciones.

## Instalación local

```bash
pip install -r requirements.txt
```

## Ejecutar dashboard

```bash
streamlit run dashboards/app_streamlit.py
```

## Ejecutar API REST

```bash
uvicorn api.api:app --reload
```

## Ejecutar pruebas

```bash
pytest tests/
```

## Ejecutar con Docker

Desde la carpeta `docker/`:

```bash
docker-compose up --build
```

El dashboard queda disponible en el puerto `8501` y la API en el puerto `8000`.
