import pandas as pd
import numpy as np
import pyodbc

# --- Step 1: Load cleaned data ---
df = pd.read_csv("Dataset/cleaned_data.csv")

# --- Step 2: Add missing numeric columns if they don't exist ---
for col in ['price', 'stock_quantity']:
    if col not in df.columns:
        df[col] = 0

# --- Step 3: Clean numeric columns ---
numeric_cols = ['price', 'rating', 'reviews_count', 'stock_quantity']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)
    df[col] = df[col].replace([np.inf, -np.inf], 0)
    df[col] = df[col].round(2)

# --- Step 4: Strip string columns ---
string_cols = ['product_id','product_name','category','brand','image_url','description','tags']
for col in string_cols:
    df[col] = df[col].astype(str).str.strip()

# --- Step 5: Connect to Azure SQL ---
server = 'ecommerce-recommender-sql-server.database.windows.net'
database = 'ecommerce_warehouse'
username = 'sqladmin'
password = 'Admin123'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
cursor = conn.cursor()

# --- Step 6: Use fast bulk insert ---
cursor.fast_executemany = True
insert_query = """
    INSERT INTO Products 
    (product_id, product_name, category, price, brand, rating, reviews_count, 
    stock_quantity, image_url, description, tags)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

data_to_insert = df[['product_id', 'product_name', 'category', 'price', 'brand',
                    'rating', 'reviews_count', 'stock_quantity', 'image_url', 'description', 'tags']].values.tolist()

cursor.executemany(insert_query, data_to_insert)

# --- Step 7: Commit and close connection ---
conn.commit()
cursor.close()
conn.close()

print("✅ Cleaned data successfully loaded into Azure SQL Data Warehouse.")