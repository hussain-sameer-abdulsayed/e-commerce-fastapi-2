
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import Product, UserProfile


class ProductReviewBase(BaseModel, table=False):
   rating: int = Field(ge=1, le=5)
   comment: Optional[str] = None
   is_approved: bool = Field(default=False)

   product_id: UUID = Field(foreign_key="products.id", index=True)
   user_profile_id: UUID = Field(foreign_key="user_profiles.id", index=True)



class ProductReview(ProductReviewBase, table=True):
   __tablename__ = "reviews" # type: ignore

   user_profile: "UserProfile" = Relationship(back_populates="product_reviews")
   product: "Product" = Relationship(back_populates="product_reviews")




