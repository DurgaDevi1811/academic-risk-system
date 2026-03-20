import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

best_acc = 0
best_model = None

for i in range(1, 4):
    model_path = os.path.join(BASE_DIR, f"model_{i}.pkl")
    acc_path = os.path.join(BASE_DIR, f"acc_{i}.txt")

    model = joblib.load(model_path)

    with open(acc_path, "r") as f:
        acc = float(f.read())

    if acc > best_acc:
        best_acc = acc
        best_model = model

global_path = os.path.join(BASE_DIR, "global_model.pkl")
joblib.dump(best_model, global_path)

print(f"✅ Best model selected with accuracy {best_acc}")