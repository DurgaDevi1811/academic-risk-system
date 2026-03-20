import pandas as pd
import os
import joblib
from sklearn.linear_model import LogisticRegression

# -----------------------------
# BASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# TRAIN LOCAL MODELS
# -----------------------------
for i in range(1, 4):
    file_path = os.path.join(BASE_DIR, f"client_{i}.csv")

    data = pd.read_csv(file_path)

    X = data[["attendance", "marks"]]
    y = data["risk"]

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    # Save model
    model_path = os.path.join(BASE_DIR, f"model_{i}.pkl")
    joblib.dump(model, model_path)

    print(f"✅ Client {i} model trained and saved at {model_path}")