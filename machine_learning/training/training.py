from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT_DIR / "machine_learning" / "datasets" / "person_distance_training.csv"
MODEL_PATH = ROOT_DIR / "person_distance_model.pkl"

data = pd.read_csv(DATASET_PATH)
data = data.rename(
    columns={
        "Distance (m)": "distance",
        "Height (px)": "height",
        "Area (px^2)": "area",
    }
)

required = ["distance", "height", "area"]
missing = [column for column in required if column not in data.columns]

if missing:
    raise ValueError(f"Dataset is missing required columns: {missing}")

data = data[required].apply(pd.to_numeric, errors="coerce")

if data.isnull().any().any():
    raise ValueError("Dataset contains missing or non-numeric values")

if not np.isfinite(data.to_numpy()).all():
    raise ValueError("Dataset contains non-finite values")

if (data[["height", "area"]] <= 0).any().any():
    raise ValueError("Height and area values must be positive")

if (data["distance"] <= 0).any():
    raise ValueError("Distance values must be positive")

if len(data) < 8 or data["distance"].nunique() < 2:
    raise ValueError("Dataset must contain at least 8 samples across 2 or more distances")

X = data[["height", "area"]]
y = data["distance"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

models = {
    "Height": ["height"],
    "Area": ["area"],
    "Combined": ["height", "area"],
}

results = {}

print("Dataset:", DATASET_PATH)
print("Dataset shape:", data.shape)
print("\nDistance distribution:")
print(y.value_counts().sort_index())
print("\nMODEL EVALUATION")
print("-" * 55)

for name, features in models.items():
    model = LinearRegression()
    model.fit(X_train[features], y_train)
    predictions = model.predict(X_test[features])

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "features": features,
    }

    print(f"\n{name} Model")
    print(f"Features: {features}")
    print(f"MAE:  {mae:.4f} m")
    print(f"RMSE: {rmse:.4f} m")
    print(f"R2:   {r2:.4f}")

best_name = min(results, key=lambda name: results[name]["MAE"])
best_features = results[best_name]["features"]

final_model = LinearRegression()
final_model.fit(X[best_features], y)

joblib.dump(
    {
        "model": final_model,
        "features": best_features,
        "model_name": best_name,
        "evaluation": {
            name: {
                "MAE": values["MAE"],
                "RMSE": values["RMSE"],
                "R2": values["R2"],
            }
            for name, values in results.items()
        },
    },
    MODEL_PATH,
)

print("\n" + "=" * 55)
print("BEST MODEL:", best_name)
print("TEST MAE:", f"{results[best_name]['MAE']:.4f} m")
print("MODEL SAVED:", MODEL_PATH)
print("=" * 55)
