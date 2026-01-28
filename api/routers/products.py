"""
Products API router
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from ..models import Product, ProductListResponse
from ..services.data_service import data_service


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Get paginated list of products"""
    products_df, total = data_service.get_products(page=page, limit=limit)
    
    products = []
    for _, row in products_df.iterrows():
        products.append(Product(
            product_id=str(row.get('ProdID', '')),
            name=str(row.get('Name', '')),
            brand=str(row.get('Brand', '')),
            category=str(row.get('Category', '')),
            rating=float(row.get('Rating', 0)),
            reviews_count=float(row.get('ReviewCount', 0)),
            image_url=str(row.get('ImageURL', '')),
            description=str(row.get('Description', '')),
            tags=str(row.get('Tags', ''))
        ))
    
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        limit=limit
    )


@router.get("/search", response_model=ProductListResponse)
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Max results")
):
    """Search products by name"""
    products_df = data_service.search_products(query=q, limit=limit)
    
    products = []
    for _, row in products_df.iterrows():
        products.append(Product(
            product_id=str(row.get('ProdID', '')),
            name=str(row.get('Name', '')),
            brand=str(row.get('Brand', '')),
            category=str(row.get('Category', '')),
            rating=float(row.get('Rating', 0)),
            reviews_count=float(row.get('ReviewCount', 0)),
            image_url=str(row.get('ImageURL', '')),
            description=str(row.get('Description', '')),
            tags=str(row.get('Tags', ''))
        ))
    
    return ProductListResponse(
        products=products,
        total=len(products),
        page=1,
        limit=limit
    )


@router.get("/names")
async def get_product_names(limit: int = Query(50, ge=1, le=500)):
    """Get list of product names for autocomplete"""
    df = data_service.get_data()
    names = df['Name'].head(limit).tolist()
    return {"names": names}
