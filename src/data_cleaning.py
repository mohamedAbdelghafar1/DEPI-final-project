import pandas as pd
import numpy as np
from pathlib import Path

script_path = Path(__file__)
script_dir = script_path.parent
root = script_dir.parent
dataset_path = root / "dataset" / "raw-data.csv"

df = pd.read_csv(dataset_path, sep='\\t|,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', quotechar='"')

df.columns = [ x.strip('"') for x in df.columns ]
df = df.dropna(axis=1, how='all')

string_columns = df.select_dtypes(include=['object']).columns
for col in string_columns:
    df[col] = df[col].str.strip('"|,')
    df[col] = df[col].replace(r'^"+$', np.nan, regex=True)

df_needed = df[['Uniq Id','Product Id','Product Rating','Product Reviews Count',
    'Product Category','Product Brand','Product Name',
    'Product Image Url','Product Description','Product Tags',
    'Product Price','Product Available Inventory']]

df_needed.rename(columns={
    'Product Id': 'product_id',
    'Product Name': 'product_name',
    'Product Category': 'category',
    'Product Brand': 'brand',
    'Product Rating': 'rating',
    'Product Reviews Count': 'reviews_count',
    'Product Image Url': 'image_url',
    'Product Description': 'description',
    'Product Tags': 'tags',
    'Product Price': 'price',
    'Product Available Inventory': 'stock_quantity'
}, inplace=True)

df_needed.drop_duplicates(subset=['product_id'], inplace=True)

df_needed.fillna({
    'rating': 0,
    'reviews_count': 0,
    'price': 0.0,
    'stock_quantity': 0,
    'category': '',
    'brand': '',
    'product_name': '',
    'image_url': '',
    'description': '',
    'tags': ''
}, inplace=True)

df_needed['rating'] = pd.to_numeric(df_needed['rating'], errors='coerce').fillna(0)
df_needed['reviews_count'] = pd.to_numeric(df_needed['reviews_count'], errors='coerce').fillna(0)
df_needed['price'] = pd.to_numeric(df_needed['price'], errors='coerce').fillna(0.0)
df_needed['stock_quantity'] = pd.to_numeric(df_needed['stock_quantity'], errors='coerce').fillna(0)

df_needed.to_csv(f'{root}/dataset/cleaned_data.csv', index=False)

print("Data cleaning completed and saved to cleaned_data.csv")