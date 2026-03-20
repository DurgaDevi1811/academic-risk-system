import pandas as pd

# Load dataset
data = pd.read_csv("data/dataset1.csv")

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
# ENSURE NUMERIC TYPES
# -----------------------------
data["attendance"] = pd.to_numeric(data["attendance"], errors="coerce")
data["marks"] = pd.to_numeric(data["marks"], errors="coerce")

data = data.dropna()

# -----------------------------
# CREATE TARGET VARIABLE (RISK)
# -----------------------------
attendance_threshold = 50
marks_threshold = 40

def assign_risk(row):
    if row["attendance"] < attendance_threshold or row["marks"] < marks_threshold:
        return 1  # At Risk
    else:
        return 0  # Safe

data["risk"] = data.apply(assign_risk, axis=1)

print("\nProcessed Data:")
print(data.head())

# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
data.to_csv("data/cleaned_data.csv", index=False)

print("\n✅ Cleaned dataset saved as cleaned_data.csv")