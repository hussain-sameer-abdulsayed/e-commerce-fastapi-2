from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine
from sqlmodel import SQLModel

# Import all models to ensure they're registered with SQLModel
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.seller_profile import SellerProfile
from app.models.address import Address
from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategoryLink
from app.models.product_review import ProductReview
from app.models.product_discount import ProductDiscount
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.coupon import Coupon
from app.models.coupon_usage import CouponUsage
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.shipment import Shipment
from app.models.shipment_discount import ShipmentDiscount
from app.models.category_discount import CategoryDiscount


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events
    """
    # Startup
    try:
        print("🚀 Starting up E-commerce API...")
        
        # Rebuild all models to ensure relationships are properly set up
        models_to_rebuild = [
            User, UserProfile, SellerProfile, Address, Category, Product,
            ProductCategoryLink, ProductReview, ProductDiscount, Cart, 
            CartItem, Coupon, CouponUsage, Order, OrderItem, Shipment, 
            ShipmentDiscount, CategoryDiscount
        ]
        
        for model in models_to_rebuild:
            try:
                model.model_rebuild()
            except Exception as e:
                print(f"⚠️  Warning: Could not rebuild {model.__name__}: {e}")
        
        print("✅ Models rebuilt successfully")
        
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


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "E-commerce API is running successfully"
    }