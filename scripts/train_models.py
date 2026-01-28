"""
Script to train and save recommendation models
Usage: python scripts/train_models.py
"""
import sys
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.data_service import data_service

def train_and_save_models():
    print("Loading data...")
    df = data_service.get_data()
    print(f"Data loaded: {len(df)} records")
    
    # Ensure artifacts directory exists
    artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model_artifacts")
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
        
    print(f"Saving models to {artifacts_dir}...")
    
    # 1. Content-Based Filtering Model (TF-IDF)
    print("Training Content-Based Model (TF-IDF)...")
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['Tags'])
    
    with open(os.path.join(artifacts_dir, 'tfidf_vectorizer.pkl'), 'wb') as f:
        pickle.dump(tfidf_vectorizer, f)
        
    with open(os.path.join(artifacts_dir, 'tfidf_matrix.pkl'), 'wb') as f:
        pickle.dump(tfidf_matrix, f)
        
    print("Content-Based Model saved.")
    
    # 2. Collaborative Filtering Model (User-Item Matrix)
    print("Training Collaborative Filtering Model (User-Item Matrix)...")
    user_item_matrix = df.pivot_table(
        index='ID', 
        columns='ProdID', 
        values='Rating', 
        aggfunc='mean'
    ).fillna(0)
    
    # We might want to save the user similarity matrix too if it's expensive to compute
    # But calculating cosine similarity on 5000x5000 might be fast enough. 
    # Let's save the matrix for now.
    
    with open(os.path.join(artifacts_dir, 'user_item_matrix.pkl'), 'wb') as f:
        pickle.dump(user_item_matrix, f)
        
    print("Collaborative Filtering Model saved.")
    
    print("All models trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_models()
