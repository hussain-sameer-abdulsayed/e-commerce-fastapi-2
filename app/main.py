from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile
from app.db.database import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

# Import all models to ensure they're registered with SQLModel
from app.models import (
    User, UserProfile, SellerProfile, Address, Category, CategoryDiscount,
    Product, ProductCategoryLink, ProductReview, ProductDiscount,
    Cart, CartItem, Coupon, CouponUsage, Order, OrderItem,
    Shipment, ShipmentDiscount
)


from app.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events
    """
    # Startup
    try:
        print("🚀 Starting up E-commerce API...")
        
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        print("✅ Database tables created successfully")
        print("🎉 E-commerce API startup complete!")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🔄 E-commerce API shutting down...")
    # Add any cleanup code here if needed




# Create FastAPI app with lifespan
app = FastAPI(
    title="E-commerce API",
    description="A comprehensive e-commerce API built with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the main API router
app.include_router(api_router, prefix="/api/v1")



