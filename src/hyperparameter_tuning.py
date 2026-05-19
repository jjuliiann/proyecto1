from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

RANDOM_STATE = 42


def optimize_random_forest(X_train, y_train):

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    pipeline = Pipeline([
        ("model", RandomForestClassifier(random_state=RANDOM_STATE))
    ])

    param_grid = {
        "model__n_estimators": [50, 100, 200],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10]
    }

    grid = GridSearchCV(
        pipeline,
        param_grid,
        cv=cv,
        scoring="f1_weighted",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    return grid


def optimize_svm(X_train, y_train):

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(random_state=RANDOM_STATE))
    ])

    param_dist = {
        "model__C": [0.1, 1, 10, 100],
        "model__kernel": ["linear", "rbf"],
        "model__gamma": ["scale", "auto"]
    }

    random_search = RandomizedSearchCV(
        pipeline,
        param_dist,
        n_iter=8,
        cv=cv,
        scoring="f1_weighted",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    random_search.fit(X_train, y_train)

    return random_search
