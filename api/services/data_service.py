"""
Data loading and preprocessing service
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional


class DataService:
    """Service for loading and managing product data"""
    
    _instance: Optional['DataService'] = None
    _data: Optional[pd.DataFrame] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess the product data"""
        if self._data is not None:
            return self._data
        
        # Find the dataset path
        base_path = Path(__file__).parent.parent.parent
        dataset_path = base_path / "dataset" / "cleaned_data.csv"
        
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at {dataset_path}")
        
        # Load the data
        df = pd.read_csv(dataset_path)
        
        # Standardize column names
        column_mapping = {
            'Uniq Id': 'ID',
            'Product Id': 'ProdID',
            'product_id': 'ProdID',
            'Product Rating': 'Rating',
            'rating': 'Rating',
            'Product Reviews Count': 'ReviewCount',
            'reviews_count': 'ReviewCount',
            'Product Category': 'Category',
            'category': 'Category',
            'Product Brand': 'Brand',
            'brand': 'Brand',
            'Product Name': 'Name',
            'product_name': 'Name',
            'Product Image Url': 'ImageURL',
            'image_url': 'ImageURL',
            'Product Description': 'Description',
            'description': 'Description',
            'Product Tags': 'Tags',
            'tags': 'Tags'
        }
        
        # Rename columns that exist
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Fill missing values
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
        if 'ReviewCount' in df.columns:
            df['ReviewCount'] = pd.to_numeric(df['ReviewCount'], errors='coerce').fillna(0)
        if 'Category' in df.columns:
            df['Category'] = df['Category'].fillna('')
        if 'Brand' in df.columns:
            df['Brand'] = df['Brand'].fillna('')
        if 'Name' in df.columns:
            df['Name'] = df['Name'].fillna('')
        if 'ImageURL' in df.columns:
            df['ImageURL'] = df['ImageURL'].fillna('')
        if 'Description' in df.columns:
            df['Description'] = df['Description'].fillna('')
        if 'Tags' in df.columns:
            df['Tags'] = df['Tags'].fillna('')
        
        # Create ID column if not exists
        if 'ID' not in df.columns:
            df['ID'] = range(1, len(df) + 1)
        
        # Create ProdID column if not exists
        if 'ProdID' not in df.columns:
            df['ProdID'] = range(1, len(df) + 1)
        
        self._data = df
        return self._data
    
    def get_data(self) -> pd.DataFrame:
        """Get the loaded data"""
        if self._data is None:
            return self.load_data()
        return self._data
    
    def get_products(self, page: int = 1, limit: int = 10) -> tuple:
        """Get paginated products"""
        df = self.get_data()
        total = len(df)
        start = (page - 1) * limit
        end = start + limit
        products = df.iloc[start:end]
        return products, total
    
    def search_products(self, query: str, limit: int = 10) -> pd.DataFrame:
        """Search products by name"""
        df = self.get_data()
        mask = df['Name'].str.lower().str.contains(query.lower(), na=False)
        return df[mask].head(limit)
    
    def get_product_by_name(self, name: str) -> Optional[pd.Series]:
        """Get a product by exact name"""
        df = self.get_data()
        matches = df[df['Name'] == name]
        if len(matches) > 0:
            return matches.iloc[0]
        return None


# Singleton instance
data_service = DataService()
