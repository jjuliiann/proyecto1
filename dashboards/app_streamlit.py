from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Dashboard de Actividad Física",
    page_icon="📊",
    layout="wide",
)


DATA_PATH = Path("data/processed/hourlySteps_eft_final.csv")


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """
    Carga y valida el dataset procesado del proyecto.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "No se encontró data/processed/hourlySteps_eft_final.csv"
        )

    df = pd.read_csv(DATA_PATH)

    columnas_requeridas = {
        "Id",
        "ActivityHour",
        "StepTotal",
        "Hora",
        "Dia",
        "FinDeSemana",
    }

    faltantes = columnas_requeridas - set(df.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas: {sorted(faltantes)}"
        )

    df["ActivityHour"] = pd.to_datetime(
        df["ActivityHour"],
        errors="coerce",
    )

    df["StepTotal"] = pd.to_numeric(
        df["StepTotal"],
        errors="coerce",
    )

    df["Hora"] = pd.to_numeric(
        df["Hora"],
        errors="coerce",
    )

    df["FinDeSemana"] = pd.to_numeric(
        df["FinDeSemana"],
        errors="coerce",
    )

    return df.dropna(
        subset=["Id", "ActivityHour", "StepTotal", "Hora"]
    )


st.title("Dashboard de Actividad Física")
st.caption(
    "Análisis interactivo de registros horarios de pasos "
    "del pipeline end-to-end."
)


try:
    df = cargar_datos()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()


# Panel lateral
st.sidebar.header("Filtros")

usuarios = sorted(df["Id"].unique().tolist())

usuarios_seleccionados = st.sidebar.multiselect(
    "Usuarios",
    options=usuarios,
    default=usuarios,
)

hora_minima, hora_maxima = st.sidebar.slider(
    "Rango de horas",
    min_value=0,
    max_value=23,
    value=(0, 23),
)

tipo_dia = st.sidebar.selectbox(
    "Tipo de día",
    options=[
        "Todos",
        "Día hábil",
        "Fin de semana",
    ],
)


df_filtrado = df.loc[
    df["Id"].isin(usuarios_seleccionados)
    & df["Hora"].between(hora_minima, hora_maxima)
].copy()


if tipo_dia == "Día hábil":
    df_filtrado = df_filtrado.loc[
        df_filtrado["FinDeSemana"] == 0
    ]

elif tipo_dia == "Fin de semana":
    df_filtrado = df_filtrado.loc[
        df_filtrado["FinDeSemana"] == 1
    ]


if df_filtrado.empty:
    st.warning(
        "No existen registros para los filtros seleccionados."
    )
    st.stop()


# KPIs principales
promedio_por_hora = (
    df_filtrado
    .groupby("Hora")["StepTotal"]
    .mean()
    .sort_values(ascending=False)
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Registros",
    f"{len(df_filtrado):,}",
)

kpi2.metric(
    "Usuarios",
    f"{df_filtrado['Id'].nunique():,}",
)

kpi3.metric(
    "Promedio de pasos",
    f"{df_filtrado['StepTotal'].mean():,.1f}",
)

kpi4.metric(
    "Hora más activa",
    f"{int(promedio_por_hora.index[0]):02d}:00",
)


st.divider()


# Gráfico por hora
st.subheader("Promedio de pasos por hora")

actividad_hora = (
    df_filtrado
    .groupby("Hora")["StepTotal"]
    .mean()
    .reset_index()
)

st.line_chart(
    actividad_hora,
    x="Hora",
    y="StepTotal",
)


# Gráfico por día
st.subheader("Promedio de pasos por día")

actividad_dia = (
    df_filtrado
    .groupby("Dia")["StepTotal"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

st.bar_chart(
    actividad_dia,
    x="Dia",
    y="StepTotal",
)


# Comparación tipo de día
st.subheader("Día hábil versus fin de semana")

comparacion_tipo_dia = (
    df_filtrado
    .assign(
        TipoDia=df_filtrado["FinDeSemana"].map(
            {
                0: "Día hábil",
                1: "Fin de semana",
            }
        )
    )
    .groupby("TipoDia")["StepTotal"]
    .mean()
    .reset_index()
)

st.bar_chart(
    comparacion_tipo_dia,
    x="TipoDia",
    y="StepTotal",
)


# Usuarios con mayor actividad
st.subheader("Usuarios con mayor promedio de actividad")

usuarios_activos = (
    df_filtrado
    .groupby("Id")["StepTotal"]
    .agg(
        promedio_pasos="mean",
        registros="count",
        maximo_pasos="max",
    )
    .reset_index()
    .sort_values(
        "promedio_pasos",
        ascending=False,
    )
)

st.dataframe(
    usuarios_activos.head(20),
    use_container_width=True,
    hide_index=True,
)


# Calidad y muestra de datos
with st.expander("Calidad y detalle del dataset"):
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Nulos",
        int(df_filtrado.isna().sum().sum()),
    )

    col2.metric(
        "Duplicados",
        int(df_filtrado.duplicated().sum()),
    )

    col3.metric(
        "Columnas",
        int(df_filtrado.shape[1]),
    )

    st.dataframe(
        df_filtrado.head(100),
        use_container_width=True,
        hide_index=True,
    )


st.download_button(
    label="Descargar datos filtrados",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="actividad_fisica_filtrada.csv",
    mime="text/csv",
)
