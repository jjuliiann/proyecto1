import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """
    Carga el dataset.
    """
    return pd.read_csv(file_path)


def classify_activity(steps):
    """
    Clasifica el nivel de actividad física.
    """
    if steps < 100:
        return "Low Activity"
    elif steps < 1000:
        return "Medium Activity"
    else:
        return "High Activity"


def prepare_data(df):
    """
    Prepara variables predictoras y objetivo.
    """
    df["ActivityLevel"] = df["StepTotal"].apply(classify_activity)

    features = [
        "Hora",
        "FinDeSemana",
        "StepTotal_scaled"
    ]

    X = df[features]
    y = df["ActivityLevel"]

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    return X, y_encoded, encoder
