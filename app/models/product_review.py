from __future__ import annotations
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from uuid import uuid4, UUID

if TYPE_CHECKING:
   from app.models.product import Product
   from app.models.user_profile import UserProfile


class ProductReviewBase(SQLModel, table=False):
   rating: int
   comment: Optional[str] = None
   is_approved: bool = Field(default=False)
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None

   product_id: UUID = Field(foreign_key="products.id", index=True)
   user_profile_id: UUID = Field(foreign_key="user_profiles.id", index=True)



class ProductReview(ProductReviewBase, table=True):
   __tablename__ = "reviews"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   user_profile: "UserProfile" = Relationship(back_populates="product_reviews")
   product: "Product" = Relationship(back_populates="product_reviews")




