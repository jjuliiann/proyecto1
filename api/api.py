from fastapi import FastAPI
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="API Proyecto Actividad Física",
    description="API REST para consultar KPIs del proyecto ETL",
    version="1.0.0"
)

DATA_PATH = Path("data/processed/hourlySteps.csv")

def cargar_datos():
    df = pd.read_csv(DATA_PATH)
    return df

@app.get("/")
def inicio():
    return {
        "mensaje": "API del proyecto ETL de actividad física funcionando correctamente"
    }

@app.get("/kpis")
def obtener_kpis():
    df = cargar_datos()

    return {
        "total_registros": int(len(df)),
        "promedio_pasos": float(round(df["StepTotal"].mean(), 2)),
        "maximo_pasos": int(df["StepTotal"].max()),
        "minimo_pasos": int(df["StepTotal"].min())
    }

@app.get("/resumen-columnas")
def resumen_columnas():
    df = cargar_datos()

    return {
        "columnas": list(df.columns),
        "cantidad_columnas": int(len(df.columns)),
        "valores_nulos": int(df.isnull().sum().sum()),
        "duplicados": int(df.duplicated().sum())
    }

@app.get("/muestra")
def muestra_datos():
    df = cargar_datos()
    return df.head(10).to_dict(orient="records")
