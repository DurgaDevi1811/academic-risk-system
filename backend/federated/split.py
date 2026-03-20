import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "..", "data", "cleaned_data.csv")

# Load correct dataset
data = pd.read_csv(data_path)

# Split using pandas (keeps columns)
clients = [data.iloc[i::3].reset_index(drop=True) for i in range(3)]

# Save each client dataset
for i, client_df in enumerate(clients):
    path = os.path.join(BASE_DIR, f"client_{i+1}.csv")
    client_df.to_csv(path, index=False)

    print(f"✅ Client {i+1} saved with columns: {client_df.columns.tolist()}")