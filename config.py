"""
Configuration management for the application
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    APP_NAME: str = "E-Commerce Recommendation System"
    VERSION: str = "1.0.0"
    
    # Paths
    # Calculate base dir relative to this file
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    # Assuming config.py is in root of project, but it is in root... wait.
    # If config.py is in d:\Courses\DEPI\Final project\DEPI-final-project\config.py
    # Then BASE_DIR is that folder.
    
    DATASET_PATH: str = "dataset/cleaned_data.csv"
    MODEL_ARTIFACTS_DIR: str = "model_artifacts"
    STATIC_DIR: str = "static"
    
    # CORS
    CORS_ORIGINS: str = "*" # Simple string for env file
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
