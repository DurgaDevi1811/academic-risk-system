import pandas as pd
import os
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# XGBoost
from xgboost import XGBClassifier

# -----------------------------
# LOAD DATA
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "..", "data", "cleaned_data.csv")

data = pd.read_csv(data_path)

print("Dataset Loaded:")
print(data.head())

# -----------------------------
# ADD CONTROLLED NOISE
# -----------------------------
np.random.seed(42)

data["attendance"] = data["attendance"] + np.random.normal(0, 8, len(data))
data["marks"] = data["marks"] + np.random.normal(0, 8, len(data))

data["attendance"] = data["attendance"].clip(0, 100)
data["marks"] = data["marks"].clip(0, 100)

# -----------------------------
# FEATURES & TARGET
# -----------------------------
X = data[["attendance", "marks"]]
y = data["risk"]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.5,
    random_state=42,
    stratify=y
)

# -----------------------------
# MODELS
# -----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=200),

    "Random Forest": RandomForestClassifier(
        n_estimators=10,     # reduced
        max_depth=2,
        min_samples_split=20,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=80,     # increased
        max_depth=3,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.2,
        reg_lambda=1,
        eval_metric="logloss"
    )
}
# -----------------------------
# TRAIN & EVALUATE
# -----------------------------
best_model = None
best_accuracy = 0
best_model_name = ""

print("\nModel Performance:\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"--- {name} ---")
    print(f"Accuracy : {acc * 100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall   : {recall:.2f}")
    print(f"F1 Score : {f1:.2f}")
    print("Confusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\n-----------------------------\n")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_model_name = name

# -----------------------------
# BEST MODEL
# -----------------------------
print("🏆 BEST MODEL")
print("-----------------------------")
print(f"Model   : {best_model_name}")
print(f"Accuracy: {best_accuracy * 100:.2f}%")
print("-----------------------------")

# -----------------------------
# SAVE MODEL
# -----------------------------
model_path = os.path.join(BASE_DIR, "student_risk_model.pkl")
joblib.dump(best_model, model_path)

print("\n✅ Model saved at:", model_path)