import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Dashboard Actividad Física",
    layout="wide"
)

st.title("Dashboard Interactivo - Actividad Física")

DATA_PATH = Path("data/processed/hourlySteps.csv")

@st.cache_data
def cargar_datos():
    df = pd.read_csv(DATA_PATH)
    return df

try:
    df = cargar_datos()

    st.sidebar.title("Menú de audiencia")

    audiencia = st.sidebar.radio(
        "Seleccione una vista",
        ["Ejecutiva", "Técnica", "Operativa"]
    )

    st.sidebar.write("Filtros disponibles")

    if "Dia" in df.columns:
        dias = st.sidebar.multiselect(
            "Filtrar por día",
            options=df["Dia"].dropna().unique(),
            default=df["Dia"].dropna().unique()
        )
        df_filtrado = df[df["Dia"].isin(dias)]
    else:
        df_filtrado = df.copy()

    if audiencia == "Ejecutiva":
        st.header("Vista Ejecutiva")

        col1, col2, col3 = st.columns(3)

        total_registros = len(df_filtrado)
        promedio_pasos = round(df_filtrado["StepTotal"].mean(), 2)
        max_pasos = int(df_filtrado["StepTotal"].max())

        col1.metric("Total de registros", total_registros)
        col2.metric("Promedio de pasos", promedio_pasos)
        col3.metric("Máximo de pasos", max_pasos)

        fig = px.histogram(
            df_filtrado,
            x="StepTotal",
            title="Distribución general de pasos"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "Esta vista está orientada a una audiencia ejecutiva. "
            "Permite observar rápidamente el comportamiento general de la actividad física "
            "mediante indicadores clave."
        )

    elif audiencia == "Técnica":
        st.header("Vista Técnica")

        col1, col2, col3 = st.columns(3)

        nulos = int(df_filtrado.isnull().sum().sum())
        duplicados = int(df_filtrado.duplicated().sum())
        columnas = len(df_filtrado.columns)

        col1.metric("Valores nulos", nulos)
        col2.metric("Duplicados", duplicados)
        col3.metric("Cantidad de columnas", columnas)

        st.subheader("Tipos de datos")

        tipos = df_filtrado.dtypes.astype(str).reset_index()
        tipos.columns = ["Columna", "Tipo de dato"]
        st.dataframe(tipos)

        st.subheader("Vista previa del dataset")
        st.dataframe(df_filtrado.head(20))

        st.write(
            "Esta vista está orientada al equipo técnico. "
            "Permite revisar la calidad del dataset, tipos de variables, valores nulos, "
            "duplicados y estructura general."
        )

    elif audiencia == "Operativa":
        st.header("Vista Operativa")

        if "Hora" in df_filtrado.columns:
            pasos_hora = df_filtrado.groupby("Hora")["StepTotal"].mean().reset_index()

            fig = px.line(
                pasos_hora,
                x="Hora",
                y="StepTotal",
                markers=True,
                title="Promedio de pasos por hora"
            )

            st.plotly_chart(fig, use_container_width=True)

        if "FinDeSemana" in df_filtrado.columns:
            pasos_fin_semana = df_filtrado.groupby("FinDeSemana")["StepTotal"].mean().reset_index()

            fig2 = px.bar(
                pasos_fin_semana,
                x="FinDeSemana",
                y="StepTotal",
                title="Promedio de pasos: semana vs fin de semana"
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.write(
            "Esta vista está orientada al análisis operativo. "
            "Permite identificar patrones de actividad física por hora y tipo de día."
        )

except FileNotFoundError:
    st.error("No se encontró el archivo data/processed/hourlySteps.csv")
except Exception as e:
    st.error(f"Ocurrió un error al cargar el dashboard: {e}")
