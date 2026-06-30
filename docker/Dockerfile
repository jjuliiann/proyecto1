# ─────────────────────────────────────────────────────────────────────
# Dockerfile — Proyecto Análisis de Actividad Física
# ─────────────────────────────────────────────────────────────────────
# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Vicente Castro, Lucas Fernandez, Julian Martinez"
LABEL description="Proyecto Ciencia de Datos - Actividad Física ETL + Dashboard + API"

# Variables de entorno para Python (sin buffers, sin .pyc)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (aprovecha cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Crear directorio de datos si no existe (será montado por volumen)
RUN mkdir -p data/raw data/processed data/og

# Exponer puertos de dashboard y API
EXPOSE 8501
EXPOSE 8000

# Healthcheck para el dashboard (puede ser sobreescrito por docker-compose)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando por defecto: iniciar el dashboard
CMD ["streamlit", "run", "dashboards/app_streamlit.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
