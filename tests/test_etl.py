import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/hourlySteps.csv")

def test_archivo_existe():
    assert DATA_PATH.exists(), "El archivo limpio no existe en data/processed"

def test_columnas_requeridas():
    df = pd.read_csv(DATA_PATH)

    columnas_requeridas = ["Id", "ActivityHour", "StepTotal"]

    for columna in columnas_requeridas:
        assert columna in df.columns, f"Falta la columna requerida: {columna}"

def test_sin_nulos_en_columnas_principales():
    df = pd.read_csv(DATA_PATH)

    assert df[["Id", "ActivityHour", "StepTotal"]].isnull().sum().sum() == 0

def test_step_total_numerico():
    df = pd.read_csv(DATA_PATH)

    assert pd.api.types.is_numeric_dtype(df["StepTotal"])

def test_sin_duplicados():
    df = pd.read_csv(DATA_PATH)

    assert df.duplicated().sum() == 0
