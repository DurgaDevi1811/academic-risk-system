import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "..", "data", "cleaned_data.csv")

data = pd.read_csv(data_path)

# Split into 3 clients
clients = np.array_split(data, 3)

# Save each client dataset
for i, client_data in enumerate(clients):
    # Ensure it's a DataFrame
    client_df = pd.DataFrame(client_data)

    path = os.path.join(BASE_DIR, f"client_{i+1}.csv")
    client_df.to_csv(path, index=False)

    print(f"Client {i+1} data saved at {path}")