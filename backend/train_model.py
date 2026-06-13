import pandas as pd

from sklearn.ensemble import RandomForestRegressor

import joblib

df = pd.read_csv(
    "data/interview_readiness.csv"
)

X = df[
    [
        "easy",
        "medium",
        "hard",
        "streak"
    ]
]

y = df["score"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "model.pkl"
)

print("Model Saved")