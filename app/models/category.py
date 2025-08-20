

from sqlmodel import Field, Relationship
from typing import List, TYPE_CHECKING
from uuid import UUID

from app.models.base_model import BaseModel
from app.models.product_category import ProductCategoryLink

if TYPE_CHECKING:
    from app.models import CategoryDiscount, Product, User



class CategoryBase(BaseModel, table=False):
    name: str = Field(index=True)
    description: str
    main_image_url: str
    
    created_by_id: UUID = Field(default=None, foreign_key="users.id")
    


class Category(CategoryBase, table=True):
    __tablename__ = "categories" # type: ignore

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

