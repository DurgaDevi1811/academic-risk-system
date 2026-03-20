import os
import joblib
import numpy as np

# -----------------------------
# BASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

weights = []
intercepts = []

# -----------------------------
# LOAD LOCAL MODELS
# -----------------------------
for i in range(1, 4):
    model_path = os.path.join(BASE_DIR, f"model_{i}.pkl")

    model = joblib.load(model_path)

    weights.append(model.coef_)
    intercepts.append(model.intercept_)

    print(f"✅ Loaded model_{i}.pkl")

# -----------------------------
# FEDERATED AVERAGING
# -----------------------------
global_weights = np.mean(weights, axis=0)
global_intercept = np.mean(intercepts, axis=0)

# -----------------------------
# DISPLAY GLOBAL MODEL
# -----------------------------
print("\n🌐 Global Model Parameters:")
print("Weights :", global_weights)
print("Intercept:", global_intercept)