from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

RANDOM_STATE = 42


def get_models():
    """
    Retorna modelos supervisados.
    """
    models = {

        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(random_state=RANDOM_STATE))
        ]),

        "Decision Tree": Pipeline([
            ("model", DecisionTreeClassifier(random_state=RANDOM_STATE))
        ]),

        "Random Forest": Pipeline([
            ("model", RandomForestClassifier(random_state=RANDOM_STATE))
        ]),

        "SVM": Pipeline([
            ("scaler", StandardScaler()),
            ("model", SVC(random_state=RANDOM_STATE))
        ]),

        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsClassifier())
        ])
    }

    return models
