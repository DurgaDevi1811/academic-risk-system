import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load global model
model_path = os.path.join(BASE_DIR, "global_model.pkl")
model = joblib.load(model_path)

# Load TEST DATA (not training data!)
test_path = os.path.join(BASE_DIR, "test_data.csv")
data = pd.read_csv(test_path)

X = data[["attendance", "marks"]]
y = data["risk"]

y_pred = model.predict(X)

acc = accuracy_score(y, y_pred)

print("\n🌍 Global Model Evaluation (NO LEAKAGE)")
print("-------------------------------------")
print(f"Accuracy: {acc * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y, y_pred))
