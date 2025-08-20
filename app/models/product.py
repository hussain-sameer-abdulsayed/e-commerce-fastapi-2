
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, List
from uuid import UUID
from decimal import Decimal

from app.models.base_model import BaseModel
from app.models.product_category import ProductCategoryLink

if TYPE_CHECKING:
    from app.models import CartItem, ProductReview, Category, SellerProfile, OrderItem, ProductDiscount


class ProductBase(BaseModel, table=False):
    name: str = Field(index=True)
    price: Decimal = Field(gt=0.00)
    stock_quantity: int = Field(default=0, ge=0)
    description: str
    main_image_url: str
    seller_profile_id: UUID = Field(foreign_key="seller_profiles.id", index=True)


class Product(ProductBase, table=True):
    __tablename__ = "products" # type: ignore
    
    product_reviews: List["ProductReview"] = Relationship(
        back_populates="product", 
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
    
    categories: List["Category"] = Relationship(
        back_populates="products", 
        link_model=ProductCategoryLink,
        sa_relationship_kwargs={'lazy': 'selectin'}
        )

    order_items: List["OrderItem"] = Relationship(back_populates="product")

    cart_items: List["CartItem"] = Relationship(
        back_populates="product", 
        cascade_delete=True
        )

    product_discounts: List["ProductDiscount"] = Relationship(
        back_populates="product",
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
        )

    seller_profile: "SellerProfile" = Relationship(back_populates="products")





