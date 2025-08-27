# app/routers/__init__.py
from fastapi import APIRouter

# Import all route modules
from .category_router import router as category_router
from .product_router import router as product_router
from .cart_router import router as cart_router
from .coupon_router import router as coupon_router
from .address_router import router as address_router
from .shipment_router import router as shipment_router
from .discount_router import router as discount_router
from .user_router import router as user_router
from .user_profile_router import router as user_profile_router
from .seller_profile_router import router as seller_profile_router
from .auth_router import router as auth_router

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

api_router.include_router(
   coupon_router,
   prefix="/coupons",
   tags=["Coupons"]
)

api_router.include_router(
   address_router,
   prefix="/addresses",
   tags=["Addresses"]
)

api_router.include_router(
   shipment_router,
   prefix="/shipments",
   tags=["Shipments"]
)

api_router.include_router(
   discount_router,
   prefix="/discounts",
   tags=["Discounts"]
)

api_router.include_router(
   user_router,
   prefix="/users",
   tags=["Users"]
)

api_router.include_router(
   user_profile_router,
   prefix="/user-profiles",
   tags=["UserProfiles"]
)

api_router.include_router(
   seller_profile_router,
   prefix="/seller-profiles",
   tags=["SellerProfiles"]
)

api_router.include_router(
   auth_router,
   prefix="/auth", 
   tags=["Authentication"]
)

# Export the main router
__all__ = ["api_router"]  # Fixed: Use double underscores
