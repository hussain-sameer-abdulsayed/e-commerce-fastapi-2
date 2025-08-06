
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4, UUID
from decimal import Decimal

from app.models.product_category import ProductCategoryLink

if TYPE_CHECKING:
    from app.models import CartItem, ProductReview, Category, SellerProfile, OrderItem, ProductDiscount


class ProductBase(SQLModel, table=False):
    name: str = Field(index=True)
    price: Decimal
    stock_quantity: int = Field(default=0)
    description: str
    main_image_url: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @property
    def is_available(self) -> bool:
        return self.stock_quantity > 0
    
    seller_profile_id: UUID = Field(foreign_key="seller_profiles.id", index=True)
    
    


class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    product_reviews: List["ProductReview"] = Relationship(
        back_populates="product", 
        cascade_delete=True
    )
    
    categories: List["Category"] = Relationship(
        back_populates="products", 
        link_model=ProductCategoryLink
        )

    order_items: List["OrderItem"] = Relationship(back_populates="product")

    cart_items: List["CartItem"] = Relationship(
        back_populates="product", 
        cascade_delete=True
        )

    product_discounts: List["ProductDiscount"] = Relationship(
        back_populates="product",
        cascade_delete=True
        )

    seller_profile: "SellerProfile" = Relationship(back_populates="products")





