from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line at the top

from app.db.database import engine
from app.db.seeder import seed_database
from sqlmodel import SQLModel

# Import all your models...
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

from app.routers import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events"""
    # Startup
    try:
        print("🚀 Starting E-commerce API...")
        
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        print("✅ Database tables created successfully")
        
        # Check if we should seed the database
        should_seed = os.getenv("SEED_DATABASE", "false").lower() == "true"
        
        if should_seed:
            print("🌱 Database seeding enabled...")
            await seed_database()
        else:
            print("🌱 Database seeding disabled (set SEED_DATABASE=true to enable)")
        
        print("🎉 E-commerce API startup complete!")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    print("👋 E-commerce API shutting down...")

# Create FastAPI app
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

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {


        
        "status": "healthy",
        "message": "E-commerce API is running successfully"
    }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

