

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4, UUID

from app.models.product_category import ProductCategoryLink

if TYPE_CHECKING:
    from app.models import CategoryDiscount, Product, User



class CategoryBase(SQLModel, table=False):
    name: str = Field(index=True)
    description: str
    main_image_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    created_by_id: UUID = Field(default=None, foreign_key="users.id")
    


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    products: List["Product"] = Relationship(
        back_populates="categories", 
        link_model=ProductCategoryLink,
        sa_relationship_kwargs={'lazy': 'selectin'}
        )

    category_discounts: List["CategoryDiscount"] = Relationship(
        back_populates="category", 
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
        )

    user: "User" = Relationship(back_populates="categories")

