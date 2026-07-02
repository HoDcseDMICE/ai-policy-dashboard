import pandas as pd
from pathlib import Path

data_dir = Path("data")
for filename in ["processed_documents.csv", "merged_policy_data.csv", "processed_opinions.csv"]:
    path = data_dir / filename
    if path.exists():
        print(f"=== {filename} ===")
        df = pd.read_csv(path, nrows=3)
        print("Columns:", list(df.columns))
        print("Shape:", pd.read_csv(path).shape)
        print("First row:")
        for col in df.columns:
            val = df.iloc[0][col]
            print(f"  {col}: {type(val).__name__} = {repr(val)[:150]}")
        print()
