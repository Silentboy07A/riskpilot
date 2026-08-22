from pathlib import Path
import pandas as pd

DATA_DIR = Path(r"C:\Users\csbal\simulated-data-raw\data")

file_path = DATA_DIR / "2018-08-23.pkl"

df = pd.read_pickle(file_path)

print("Shape:", df.shape)

print("\nColumns:")
for column in df.columns:
    print(f"- {column}")

print("\nFirst 5 rows:")
print(df.head())

print("\nFraud count:", df["TX_FRAUD"].sum())
print("Fraud rate:", f"{df['TX_FRAUD'].mean() * 100:.4f}%")