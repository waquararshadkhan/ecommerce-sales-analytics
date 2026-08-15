# %% Setup
import pandas as pd

orders = pd.read_csv("data/List of Orders.csv")
details = pd.read_csv("data/Order Details.csv")
target = pd.read_csv("data/Sales target.csv")

# %% 1. Drop the 60 fully-blank trailing rows in Orders
orders = orders.dropna(how="all")
print(orders.shape)   # expect (500, 5)

# %% 2. Fix Order Date: it's DD-MM-YYYY text, must tell pandas explicitly
orders["Order Date"] = pd.to_datetime(orders["Order Date"], format="%d-%m-%Y")
print(orders.dtypes["Order Date"])   # expect datetime64
print(orders["Order Date"].min(), orders["Order Date"].max())

# %% 3. Fix Sales Target month: 'Apr-18' -> proper date (use 1st of month)
target["Month of Order Date"] = pd.to_datetime(target["Month of Order Date"], format="%b-%y")
print(target.head())

# %% 4. Sanity check: row counts after cleaning
print("Orders:", orders.shape)
print("Details:", details.shape)
print("Target:", target.shape)

# %% 5. Merge Orders + Order Details on Order ID
sales = orders.merge(details, on="Order ID", how="inner")
print(sales.shape)   # expect (1500, 10) -> 5+6 cols minus 1 shared key
print(sales.head())

# %% 6. Add a Month column (first-of-month) so it can later match Target
sales["Month"] = sales["Order Date"].dt.to_period("M").dt.to_timestamp()
print(sales[["Order Date", "Month"]].head())

# %% 7. Save cleaned files for the next stage (loading into MySQL)
sales.to_csv("data/cleaned_sales.csv", index=False)
target.to_csv("data/cleaned_target.csv", index=False)
print("Saved cleaned_sales.csv and cleaned_target.csv")

# %% 8. Connect to MySQL
import os
from sqlalchemy import create_engine

password = os.environ["MYSQL_PWD"]
user = "root"
host = "localhost"
port = 3306
db = "ecommerce_sales"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
print("engine created")

# %% 9. Push the cleaned tables into MySQL (replaces table each run)
sales.to_sql("sales", engine, if_exists="replace", index=False)
target.to_sql("sales_target", engine, if_exists="replace", index=False)
print("Loaded 'sales' and 'sales_target' tables into MySQL")
