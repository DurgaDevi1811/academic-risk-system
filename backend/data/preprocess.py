import pandas as pd
import numpy as np
import os

# -----------------------------
# LOAD DATASET (CORRECT PATH)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "dataset1", "student-mat.csv")

data = pd.read_csv(file_path,sep=';')

print("Original Data:")
print(data.head())

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

print("\nColumns after cleaning:")
print(data.columns)

# -----------------------------
# HANDLE MISSING VALUES
# -----------------------------
data = data.dropna()

# -----------------------------
# CREATE REQUIRED FEATURES
# -----------------------------
# Convert G3 (0–20 scale) to percentage (0–100)
data["marks"] = (pd.to_numeric(data["g3"], errors="coerce") / 20) * 100

# Simulate attendance (since dataset doesn't have it)
np.random.seed(42)
data["attendance"] = np.random.randint(30, 100, size=len(data))

# Remove invalid rows
data = data.dropna(subset=["marks", "attendance"])

# -----------------------------
# CREATE TARGET VARIABLE (RISK)
# -----------------------------
attendance_threshold = 50
marks_threshold = 40  # now correctly in percentage

def assign_risk(row):
    if row["attendance"] < attendance_threshold or row["marks"] < marks_threshold:
        return 1  # At Risk
    else:
        return 0  # Safe

data["risk"] = data.apply(assign_risk, axis=1)

# -----------------------------
# SELECT FINAL FEATURES
# -----------------------------
final_data = data[["attendance", "marks", "risk"]]

print("\nProcessed Data:")
print(final_data.head())

# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
output_path = os.path.join(BASE_DIR, "cleaned_data.csv")
final_data.to_csv(output_path, index=False)

print("\n✅ Cleaned dataset saved at:", output_path)