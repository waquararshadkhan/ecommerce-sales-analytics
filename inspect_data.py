import pandas as pd

# Dictionary mapping a short name -> file path
files = {
    "Orders": "data/List of Orders.csv",
    "Order Details": "data/Order Details.csv",
    "Sales Target": "data/Sales target.csv",
}

for name, path in files.items():
    print("=" * 60)
    print(f"DATASET: {name}")
    print("=" * 60)

    df = pd.read_csv(path)

    print(f"\nShape (rows, columns): {df.shape}")

    print(f"\nColumn names:\n{list(df.columns)}")

    print(f"\nData types:\n{df.dtypes}")

    print(f"\nMissing values per column:\n{df.isnull().sum()}")

    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    print(f"\nFirst 3 rows:\n{df.head(3)}")
    print("\n")