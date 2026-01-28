"""
Recommendation algorithms service
Extracted from the EDA and models notebook
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional, List

from .data_service import data_service


class RecommenderService:
    """Service for generating product recommendations"""
    
    _instance: Optional['RecommenderService'] = None
    _tfidf_matrix: Optional[np.ndarray] = None
    _tfidf_vectorizer: Optional[TfidfVectorizer] = None
    _user_item_matrix: Optional[pd.DataFrame] = None
    _user_similarity: Optional[np.ndarray] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _build_content_model(self) -> None:
        """Build or load TF-IDF model for content-based filtering"""
        if self._tfidf_matrix is not None:
            return
            
        import pickle
        import os
        
        artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "model_artifacts")
        vectorizer_path = os.path.join(artifacts_dir, 'tfidf_vectorizer.pkl')
        matrix_path = os.path.join(artifacts_dir, 'tfidf_matrix.pkl')
        
        if os.path.exists(vectorizer_path) and os.path.exists(matrix_path):
            try:
                with open(vectorizer_path, 'rb') as f:
                    self._tfidf_vectorizer = pickle.load(f)
                with open(matrix_path, 'rb') as f:
                    self._tfidf_matrix = pickle.load(f)
                print("Loaded content-based models from disk")
                return
            except Exception as e:
                print(f"Error loading models: {e}. Retraining...")
        
        print("Training content-based models...")
        df = data_service.get_data()
        
        # Create TF-IDF vectorizer for product tags
        self._tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self._tfidf_matrix = self._tfidf_vectorizer.fit_transform(df['Tags'])
    
    def _build_collaborative_model(self) -> None:
        """Build or load user-item matrix for collaborative filtering"""
        if self._user_item_matrix is not None:
            return
            
        import pickle
        import os
        
        artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "model_artifacts")
        matrix_path = os.path.join(artifacts_dir, 'user_item_matrix.pkl')
        
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, 'rb') as f:
                    self._user_item_matrix = pickle.load(f)
                # Calculate similarity on the fly as it might be large to save, or save it too if needed
                # For now let's calculate it
                self._user_similarity = cosine_similarity(self._user_item_matrix)
                print("Loaded collaborative filtering Matrix from disk")
                return
            except Exception as e:
                print(f"Error loading collaborative models: {e}. Retraining...")
        
        print("Training collaborative models...")
        df = data_service.get_data()
        
        # Create user-item matrix
        self._user_item_matrix = df.pivot_table(
            index='ID', 
            columns='ProdID', 
            values='Rating', 
            aggfunc='mean'
        ).fillna(0)
        
        # Calculate user similarity
        self._user_similarity = cosine_similarity(self._user_item_matrix)
    
    def content_based_recommendations(
        self, 
        item_name: str, 
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        Get content-based recommendations for a product
        Uses TF-IDF on product tags and cosine similarity
        """
        df = data_service.get_data()
        
        # Check if item exists
        if item_name not in df['Name'].values:
            return pd.DataFrame()
        
        # Build the model if not already built
        self._build_content_model()
        
        # Find the index of the item
        item_index = df[df['Name'] == item_name].index[0]
        
        # Calculate cosine similarity for this item
        cosine_similarities = cosine_similarity(
            self._tfidf_matrix[item_index:item_index+1], 
            self._tfidf_matrix
        ).flatten()
        
        # Get similar items (enumerated)
        similar_items = list(enumerate(cosine_similarities))
        
        # Sort by similarity score in descending order
        similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
        
        # Get top N similar items (excluding the item itself)
        top_similar_items = similar_items[1:top_n+1]
        
        # Get indices of recommended items
        recommended_indices = [x[0] for x in top_similar_items]
        
        # Return recommendation details
        return df.iloc[recommended_indices][[
            'Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'ProdID'
        ]]
    
    def collaborative_filtering_recommendations(
        self, 
        user_id: int, 
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        Get collaborative filtering recommendations for a user
        Uses user-item matrix and cosine similarity
        """
        df = data_service.get_data()
        
        # Build the model if not already built
        self._build_collaborative_model()
        
        # Check if user exists in the matrix
        if user_id not in self._user_item_matrix.index:
            # Return popular items if user not found
            return df.nlargest(top_n, 'Rating')[[
                'Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'ProdID'
            ]]
        
        # Find the index of the target user
        target_user_index = self._user_item_matrix.index.get_loc(user_id)
        
        # Get similarity scores for this user
        user_similarities = self._user_similarity[target_user_index]
        
        # Sort users by similarity in descending order (excluding target user)
        similar_user_indices = user_similarities.argsort()[::-1][1:]
        
        # Generate recommendations based on similar users
        recommended_items = []
        
        for user_index in similar_user_indices:
            # Get items rated by similar user but not by target user
            rated_by_similar = self._user_item_matrix.iloc[user_index]
            not_rated_by_target = (
                (rated_by_similar == 0) & 
                (self._user_item_matrix.iloc[target_user_index] == 0)
            )
            
            # Add recommended items
            new_items = self._user_item_matrix.columns[not_rated_by_target][:top_n]
            recommended_items.extend(new_items.tolist())
            
            # Stop if we have enough recommendations
            if len(recommended_items) >= top_n * 2:
                break
        
        # Get unique recommended items
        recommended_items = list(dict.fromkeys(recommended_items))[:top_n]
        
        # Get product details
        result = df[df['ProdID'].isin(recommended_items)][[
            'Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'ProdID'
        ]]
        
        return result.head(top_n)
    
    def hybrid_recommendations(
        self, 
        user_id: int, 
        item_name: str, 
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        Get hybrid recommendations combining content-based and collaborative filtering
        """
        # Get content-based recommendations
        content_rec = self.content_based_recommendations(item_name, top_n)
        
        # Get collaborative filtering recommendations
        collab_rec = self.collaborative_filtering_recommendations(user_id, top_n)
        
        # Combine and deduplicate
        if len(content_rec) > 0 and len(collab_rec) > 0:
            hybrid_rec = pd.concat([content_rec, collab_rec]).drop_duplicates(subset=['Name'])
        elif len(content_rec) > 0:
            hybrid_rec = content_rec
        else:
            hybrid_rec = collab_rec
        
        return hybrid_rec.head(top_n)
    
    def get_popular_products(self, top_n: int = 10) -> pd.DataFrame:
        """Get most popular products by rating"""
        df = data_service.get_data()
        return df.nlargest(top_n, 'Rating')[[
            'Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'ProdID'
        ]]


# Singleton instance
recommender_service = RecommenderService()
