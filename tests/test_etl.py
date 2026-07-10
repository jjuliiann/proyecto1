from pathlib import Path

import pandas as pd


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
    assert DATA_PATH.exists(), (
        "No existe data/processed/hourlySteps_eft_final.csv"
    )

    df = pd.read_csv(DATA_PATH)

    assert not df.empty, "El dataset procesado está vacío."

    return df


def test_dataset_exists():
    assert DATA_PATH.exists()


def test_dataset_not_empty():
    df = cargar_datos()
    assert len(df) > 0


def test_required_columns():
    df = cargar_datos()

    faltantes = COLUMNAS_REQUERIDAS - set(df.columns)

    assert not faltantes, (
        f"Faltan columnas requeridas: {sorted(faltantes)}"
    )


def test_no_nulls_in_critical_columns():
    df = cargar_datos()

    columnas_criticas = [
        "Id",
        "ActivityHour",
        "StepTotal",
        "Hora",
    ]

    assert df[columnas_criticas].isna().sum().sum() == 0


def test_no_duplicate_user_hour():
    df = cargar_datos()

    duplicados = df.duplicated(
        subset=["Id", "ActivityHour"]
    ).sum()

    assert duplicados == 0


def test_step_total_is_numeric():
    df = cargar_datos()

    pasos = pd.to_numeric(
        df["StepTotal"],
        errors="coerce",
    )

    assert pasos.notna().all()


def test_step_total_has_valid_range():
    df = cargar_datos()

    pasos = pd.to_numeric(
        df["StepTotal"],
        errors="coerce",
    )

    assert (pasos >= 0).all()


def test_hour_range():
    df = cargar_datos()

    horas = pd.to_numeric(
        df["Hora"],
        errors="coerce",
    )

    assert horas.between(0, 23).all()


def test_weekend_is_binary():
    df = cargar_datos()

    valores = set(
        pd.to_numeric(
            df["FinDeSemana"],
            errors="coerce",
        ).dropna().unique()
    )

    assert valores.issubset({0, 1})
