import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "..", "data", "cleaned_data.csv")

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv(data_path)

print("📂 Data Loaded Successfully")
print(data.head())

# -----------------------------
# CREATE GLOBAL TEST SET (NO LEAKAGE)
# -----------------------------
train_data, test_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42,
    stratify=data["risk"]
)

# Save test data
test_path = os.path.join(BASE_DIR, "test_data.csv")
test_data.to_csv(test_path, index=False)

print("\n✅ Test dataset created")

# -----------------------------
# STRATIFIED CLIENT SPLIT
# -----------------------------
clients = 3
skf = StratifiedKFold(n_splits=clients, shuffle=True, random_state=42)

for i, (_, idx) in enumerate(skf.split(train_data, train_data["risk"])):
    client_data = train_data.iloc[idx].reset_index(drop=True)

    path = os.path.join(BASE_DIR, f"client_{i+1}.csv")
    client_data.to_csv(path, index=False)

print("✅ Stratified client datasets created")

# -----------------------------
# DISTRIBUTION CHECK (IMPORTANT)
# -----------------------------
print("\n📊 Distribution Check:")

print("\nTest Data Distribution:")
print(test_data["risk"].value_counts(normalize=True))

for i in range(clients):
    client_path = os.path.join(BASE_DIR, f"client_{i+1}.csv")
    client_df = pd.read_csv(client_path)

    print(f"\nClient {i+1} Distribution:")
    print(client_df["risk"].value_counts(normalize=True))