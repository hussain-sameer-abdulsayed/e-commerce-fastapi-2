# app/routers/__init__.py
from fastapi import APIRouter

# Import all route modules
from .category_router import router as category_router
# Add more routers as you create them:
# from .user_router import router as user_router
# from .product_router import router as product_router

# Create main API router
api_router = APIRouter()

# Include all routers with their prefixes and tags
# Prefix is defined HERE, not in individual routers
api_router.include_router(
    category_router,
    prefix="/categories",  # This is the ONLY place to define the prefix
    tags=["Categories"]    # Consistent tag naming
)

# Add more routers as you create them:
# api_router.include_router(
#     user_router,
#     prefix="/users",
#     tags=["Users"]
# )

# api_router.include_router(
#     product_router,
#     prefix="/products", 
#     tags=["Products"]
# )

# Export the main router
__all__ = ["api_router"]  # Fixed: Use double underscores