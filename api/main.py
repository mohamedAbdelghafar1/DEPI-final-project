"""
E-Commerce Recommendation System API
FastAPI application entry point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routers import products, recommendations
from .services.data_service import data_service
from .models import HealthResponse


# Create FastAPI application
app = FastAPI(
    title="E-Commerce Recommendation System API",
    description="""
    REST API for the E-Commerce Recommendation System.
    
    ## Features
    - **Products**: Browse and search products
    - **Recommendations**: Get personalized product recommendations
    """,
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(recommendations.router)

# Mount static files
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(base_path, "static")

if os.path.exists(static_path):
    app.mount("/css", StaticFiles(directory=os.path.join(static_path, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(static_path, "js")), name="js")

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    print("Loading product data...")
    try:
        data_service.load_data()
        print(f"Loaded {len(data_service.get_data())} products")
    except Exception as e:
        print(f"Error loading data: {e}")


@app.get("/", tags=["Frontend"])
async def root():
    """Serve the frontend application"""
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. API is running."}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check if data is loaded
        data = data_service.get_data()
        if len(data) > 0:
            return HealthResponse(
                status="healthy",
                message=f"API is running. {len(data)} products loaded."
            )
        else:
            return HealthResponse(
                status="degraded",
                message="API is running but no products loaded."
            )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Error: {str(e)}"
        )
