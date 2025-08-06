
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID
from app.models.discount_base import DiscountBase


if TYPE_CHECKING:
   from app.models import Category


class CategoryDiscount(DiscountBase, table=True):
   __tablename__ = "category_discounts"
   category_id: UUID = Field(foreign_key="categories.id", index=True)
   category : "Category" = Relationship(back_populates="category_discounts")





