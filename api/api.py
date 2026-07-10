from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API de Actividad Física",
    description=(
        "API REST para consultar datos procesados, KPIs "
        "y análisis del proyecto end-to-end."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATA_PATH = Path("data/processed/hourlySteps_eft_final.csv")

COLUMNAS_REQUERIDAS = {
    "Id",
    "ActivityHour",
    "StepTotal",
    "Hora",
    "Dia",
    "FinDeSemana",
}


def cargar_datos() -> pd.DataFrame:
    """
    Carga y valida el dataset procesado utilizado por la API.
    """
    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail=(
                "No se encontró el dataset procesado. "
                "Ejecute primero el notebook EFT."
            ),
        )

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer el dataset: {error}",
        ) from error

    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="El dataset procesado está vacío.",
        )

    faltantes = COLUMNAS_REQUERIDAS - set(df.columns)

    if faltantes:
        raise HTTPException(
            status_code=500,
            detail=f"Faltan columnas requeridas: {sorted(faltantes)}",
        )

    df["StepTotal"] = pd.to_numeric(
        df["StepTotal"],
        errors="coerce",
    )

    df["Hora"] = pd.to_numeric(
        df["Hora"],
        errors="coerce",
    )

    return df


@app.get("/", tags=["Estado"])
def inicio():
    """
    Verifica que la API esté funcionando.
    """
    return {
        "estado": "ok",
        "mensaje": "API de actividad física funcionando correctamente",
        "version": app.version,
        "documentacion": "/docs",
    }


@app.get("/health", tags=["Estado"])
def health_check():
    """
    Comprueba la disponibilidad y calidad básica del dataset.
    """
    df = cargar_datos()

    return {
        "estado": "saludable",
        "dataset_disponible": True,
        "total_registros": int(len(df)),
        "columnas": int(df.shape[1]),
        "nulos_criticos": int(
            df[["Id", "ActivityHour", "StepTotal"]]
            .isna()
            .sum()
            .sum()
        ),
    }


@app.get("/kpis", tags=["Indicadores"])
def obtener_kpis():
    """
    Retorna los principales indicadores de actividad física.
    """
    df = cargar_datos()

    promedio_por_hora = (
        df.groupby("Hora")["StepTotal"]
        .mean()
        .sort_values(ascending=False)
    )

    return {
        "total_registros": int(len(df)),
        "usuarios_unicos": int(df["Id"].nunique()),
        "promedio_pasos_hora": round(
            float(df["StepTotal"].mean()),
            2,
        ),
        "mediana_pasos_hora": round(
            float(df["StepTotal"].median()),
            2,
        ),
        "maximo_pasos": int(df["StepTotal"].max()),
        "minimo_pasos": int(df["StepTotal"].min()),
        "hora_mayor_actividad": int(promedio_por_hora.index[0]),
        "promedio_dia_habil": round(
            float(
                df.loc[
                    df["FinDeSemana"] == 0,
                    "StepTotal",
                ].mean()
            ),
            2,
        ),
        "promedio_fin_semana": round(
            float(
                df.loc[
                    df["FinDeSemana"] == 1,
                    "StepTotal",
                ].mean()
            ),
            2,
        ),
    }


@app.get("/resumen-columnas", tags=["Calidad"])
def resumen_columnas():
    """
    Entrega información de estructura y calidad del dataset.
    """
    df = cargar_datos()

    detalle = []

    for columna in df.columns:
        detalle.append(
            {
                "columna": columna,
                "tipo": str(df[columna].dtype),
                "nulos": int(df[columna].isna().sum()),
                "valores_unicos": int(
                    df[columna].nunique(dropna=True)
                ),
            }
        )

    return {
        "cantidad_columnas": int(df.shape[1]),
        "valores_nulos_totales": int(
            df.isna().sum().sum()
        ),
        "duplicados": int(df.duplicated().sum()),
        "detalle": detalle,
    }


@app.get("/muestra", tags=["Datos"])
def muestra_datos(
    limite: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Cantidad de registros a retornar",
    )
):
    """
    Retorna una muestra limitada del dataset.
    """
    df = cargar_datos()

    return df.head(limite).to_dict(
        orient="records"
    )


@app.get("/actividad-por-hora", tags=["Análisis"])
def actividad_por_hora():
    """
    Retorna estadísticas agrupadas por hora del día.
    """
    df = cargar_datos()

    resumen = (
        df.groupby("Hora")["StepTotal"]
        .agg(
            registros="count",
            promedio="mean",
            mediana="median",
            maximo="max",
        )
        .reset_index()
        .sort_values("Hora")
    )

    resumen["promedio"] = resumen["promedio"].round(2)
    resumen["mediana"] = resumen["mediana"].round(2)

    return resumen.to_dict(
        orient="records"
    )


@app.get("/actividad-por-dia", tags=["Análisis"])
def actividad_por_dia():
    """
    Retorna estadísticas agrupadas por día.
    """
    df = cargar_datos()

    resumen = (
        df.groupby("Dia")["StepTotal"]
        .agg(
            registros="count",
            promedio="mean",
            mediana="median",
            maximo="max",
        )
        .reset_index()
        .sort_values(
            "promedio",
            ascending=False,
        )
    )

    resumen["promedio"] = resumen["promedio"].round(2)
    resumen["mediana"] = resumen["mediana"].round(2)

    return resumen.to_dict(
        orient="records"
    )


@app.get("/usuario/{usuario_id}", tags=["Usuarios"])
def resumen_usuario(usuario_id: int):
    """
    Entrega indicadores de un usuario específico.
    """
    df = cargar_datos()

    usuario = df.loc[
        df["Id"] == usuario_id
    ].copy()

    if usuario.empty:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado.",
        )

    return {
        "usuario_id": usuario_id,
        "registros": int(len(usuario)),
        "promedio_pasos": round(
            float(usuario["StepTotal"].mean()),
            2,
        ),
        "mediana_pasos": round(
            float(usuario["StepTotal"].median()),
            2,
        ),
        "maximo_pasos": int(
            usuario["StepTotal"].max()
        ),
        "horas_registradas": int(
            usuario["ActivityHour"].nunique()
        ),
    }


@app.get("/buscar", tags=["Datos"])
def buscar_registros(
    hora: Optional[int] = Query(
        default=None,
        ge=0,
        le=23,
    ),
    fin_de_semana: Optional[int] = Query(
        default=None,
        ge=0,
        le=1,
    ),
    pasos_minimos: Optional[int] = Query(
        default=None,
        ge=0,
    ),
    limite: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
):
    """
    Filtra registros por hora, tipo de día y pasos mínimos.
    """
    df = cargar_datos()

    filtrado = df.copy()

    if hora is not None:
        filtrado = filtrado.loc[
            filtrado["Hora"] == hora
        ]

    if fin_de_semana is not None:
        filtrado = filtrado.loc[
            filtrado["FinDeSemana"] == fin_de_semana
        ]

    if pasos_minimos is not None:
        filtrado = filtrado.loc[
            filtrado["StepTotal"] >= pasos_minimos
        ]

    return {
        "total_encontrados": int(len(filtrado)),
        "registros": filtrado.head(limite).to_dict(
            orient="records"
        ),
    }
