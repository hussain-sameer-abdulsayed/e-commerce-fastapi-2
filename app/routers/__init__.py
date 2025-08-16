# app/routers/__init__.py
from fastapi import APIRouter

# Import all route modules
from .category_router import router as category_router
from .product_router import router as product_router
from .cart_router import router as cart_router


# Create main API router
api_router = APIRouter()

# Include all routers with their prefixes and tags
api_router.include_router(
    category_router,
    prefix="/categories",
    tags=["Categories"]
)

api_router.include_router(
   product_router,
   prefix="/products",
   tags=["Products"]
)

api_router.include_router(
   cart_router,
   prefix="/carts",
   tags=["Carts"]
)



# Export the main router
__all__ = ["api_router"]  # Fixed: Use double underscores