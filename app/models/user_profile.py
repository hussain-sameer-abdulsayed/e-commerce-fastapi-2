
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, List
from datetime import date
from uuid import UUID
from app.enums.enums import Gender
from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import ProductReview, User, Order, Image

   

class UserProfileBase(BaseModel, table=False):
   bio: str
   gender: Gender = Field(default=Gender.MALE)
   birth_date: date
   user_id: UUID = Field(foreign_key="users.id", index=True)


class UserProfile(UserProfileBase, table=True):
   __tablename__ = "user_profiles" # type: ignore

   user: "User" = Relationship(back_populates="user_profile")
   orders: List["Order"] = Relationship(back_populates="user_profile")
   product_reviews: List["ProductReview"] = Relationship(
      back_populates="user_profile", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
   )
   images: List["Image"] = Relationship(
      back_populates= "user_profile",
      cascade_delete= True,
      sa_relationship_kwargs={'lazy': 'selectin'}
   )






