# Arquitectura del Sistema

## Descripción general

Este proyecto desarrolla una solución end-to-end para el análisis de actividad física. La solución integra distintas fuentes de datos, ejecuta un pipeline ETL, disponibiliza resultados mediante una API REST, visualiza indicadores en un dashboard interactivo y considera despliegue mediante Docker.

## Fuentes de datos

Las fuentes se organizan en tres niveles:

1. `data/raw/hourlySteps_sucio.csv`: dataset sucio utilizado para demostrar limpieza, validación y transformación.
2. `data/og/hourlySteps_merged.csv`: dataset original consolidado utilizado como referencia.
3. `data/processed/hourlySteps.csv`: dataset procesado utilizado por el dashboard, la API y las pruebas automatizadas.

## Flujo de arquitectura

1. El notebook extrae datos desde archivos CSV.
2. El pipeline valida columnas requeridas y tipos de datos.
3. Se realiza limpieza de valores nulos, duplicados y formato de fechas.
4. Se generan variables derivadas como hora, día y fin de semana.
5. El resultado limpio queda almacenado en `data/processed/`.
6. El dashboard consume el dataset procesado.
7. La API REST expone KPIs y muestras de datos.
8. Docker permite ejecutar los servicios de forma reproducible.

## Componentes del repositorio

```text
data/          Datos raw, originales y procesados
notebooks/     Notebooks principales del proyecto
src/           Scripts auxiliares del proyecto
dashboards/    Dashboard interactivo en Streamlit
api/           API REST con FastAPI
docker/        Dockerfile y docker-compose
tests/         Pruebas automatizadas
docs/          Documentación técnica
