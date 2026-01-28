"""
Recommendations API router
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from ..models import Product, RecommendationResponse
from ..services.recommender import recommender_service
from ..services.data_service import data_service


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def _df_to_products(df) -> list:
    """Convert DataFrame rows to Product objects"""
    products = []
    for _, row in df.iterrows():
        products.append(Product(
            product_id=str(row.get('ProdID', '')),
            name=str(row.get('Name', '')),
            brand=str(row.get('Brand', '')),
            rating=float(row.get('Rating', 0)),
            reviews_count=float(row.get('ReviewCount', 0)),
            image_url=str(row.get('ImageURL', ''))
        ))
    return products


@router.get("/content-based", response_model=RecommendationResponse)
async def get_content_based_recommendations(
    product_name: str = Query(..., description="Product name to get recommendations for"),
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations")
):
    """
    Get content-based recommendations for a product.
    Uses TF-IDF on product tags and cosine similarity.
    """
    # Check if product exists
    product = data_service.get_product_by_name(product_name)
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Product '{product_name}' not found. Use /products/names to get valid product names."
        )
    
    # Get recommendations
    rec_df = recommender_service.content_based_recommendations(product_name, top_n)
    
    if len(rec_df) == 0:
        # Return popular products as fallback
        rec_df = recommender_service.get_popular_products(top_n)
    
    products = _df_to_products(rec_df)
    
    return RecommendationResponse(
        recommendations=products,
        recommendation_type="content-based",
        total=len(products)
    )


@router.get("/collaborative", response_model=RecommendationResponse)
async def get_collaborative_recommendations(
    user_id: int = Query(..., description="User ID to get recommendations for"),
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations")
):
    """
    Get collaborative filtering recommendations for a user.
    Uses user-item matrix and cosine similarity.
    """
    # Get recommendations
    rec_df = recommender_service.collaborative_filtering_recommendations(user_id, top_n)
    
    products = _df_to_products(rec_df)
    
    return RecommendationResponse(
        recommendations=products,
        recommendation_type="collaborative",
        total=len(products)
    )


@router.get("/hybrid", response_model=RecommendationResponse)
async def get_hybrid_recommendations(
    user_id: int = Query(..., description="User ID"),
    product_name: str = Query(..., description="Product name"),
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations")
):
    """
    Get hybrid recommendations combining content-based and collaborative filtering.
    """
    # Get recommendations 
    rec_df = recommender_service.hybrid_recommendations(user_id, product_name, top_n)
    
    if len(rec_df) == 0:
        # Return popular products as fallback
        rec_df = recommender_service.get_popular_products(top_n)
    
    products = _df_to_products(rec_df)
    
    return RecommendationResponse(
        recommendations=products,
        recommendation_type="hybrid",
        total=len(products)
    )


@router.get("/popular", response_model=RecommendationResponse)
async def get_popular_products(
    top_n: int = Query(10, ge=1, le=50, description="Number of products")
):
    """Get most popular products by rating"""
    rec_df = recommender_service.get_popular_products(top_n)
    products = _df_to_products(rec_df)
    
    return RecommendationResponse(
        recommendations=products,
        recommendation_type="popular",
        total=len(products)
    )
