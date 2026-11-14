
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


data = pd.read_csv("person_distance_data.csv")


print("Dataset shape:", data.shape)
print("\nDistance distribution:")
print(data["distance"].value_counts().sort_index())

required = ["distance", "height", "area"]

if not all(col in data.columns for col in required):
    raise ValueError("CSV must contain distance, height, area columns")

if data[required].isnull().any().any():
    raise ValueError("Dataset contains missing values")

if len(data) != 120:
    raise ValueError(f"Expected 120 samples, found {len(data)}")

X = data[["height", "area"]]
y = data["distance"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


models = {
    "Height": ["height"],
    "Area": ["area"],
    "Combined": ["height", "area"]
}

results = {}
trained_models = {}

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
        "R2": r2
    }

    trained_models[name] = model

    print(f"\n{name} Model")
    print(f"MAE:  {mae:.4f} m")
    print(f"RMSE: {rmse:.4f} m")
    print(f"R2:   {r2:.4f}")


best_name = min(results, key=lambda name: results[name]["MAE"])

print("\n" + "=" * 55)
print("BEST MODEL:", best_name)
print("TEST MAE:", results[best_name]["MAE"], "metres")
print("=" * 55)


best_features = models[best_name]

final_model = LinearRegression()
final_model.fit(X[best_features], y)

joblib.dump({
    "model": final_model,
    "features": best_features,
    "model_name": best_name
}, "person_distance_model.pkl")

print("\nFinal model saved successfully!")
print("File: person_distance_model.pkl")
