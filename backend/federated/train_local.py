import pandas as pd
import os
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

    # Split client data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Train model
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Accuracy
    acc = accuracy_score(y_test, y_pred)

    # Save model
    model_path = os.path.join(BASE_DIR, f"model_{i}.pkl")
    joblib.dump(model, model_path)

    # Save accuracy
    acc_path = os.path.join(BASE_DIR, f"acc_{i}.txt")
    with open(acc_path, "w") as f:
        f.write(str(acc))

    print(f"✅ Client {i} model trained")
    print(f"   Accuracy: {acc*100:.2f}%")