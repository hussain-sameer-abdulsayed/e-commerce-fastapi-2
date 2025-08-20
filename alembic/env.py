import sys
from pathlib import Path
import asyncio
import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from dotenv import load_dotenv


# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your SQLModel metadata
from sqlmodel import SQLModel

# Import all your models so they are registered with SQLModel.metadata
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

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

def get_url():
    """Get database URL from environment variables"""
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:078@localhost:5432/fastapi")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using async engine."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()



