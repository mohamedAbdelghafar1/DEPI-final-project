"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List


class Product(BaseModel):
    """Product model"""
    product_id: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    rating: float = 0.0
    reviews_count: float = 0.0
    image_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None


class ProductListResponse(BaseModel):
    """Response model for product list"""
    products: List[Product]
    total: int
    page: int
    limit: int


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    recommendations: List[Product]
    recommendation_type: str
    total: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
