
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from uuid import uuid4, UUID
from app.enums.enums import Gender

if TYPE_CHECKING:
   from app.models import ProductReview, User, Order

   

class UserProfileBase(SQLModel, table=False):
   main_image_url: str
   bio: str
   gender: Gender = Field(default=Gender.MALE)
   birth_date: datetime
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None
   
   user_id: UUID = Field(foreign_key="users.id", index=True)
   


class UserProfile(UserProfileBase, table=True):
   __tablename__ = "user_profiles"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   user: "User" = Relationship(back_populates="user_profile")
   orders: List["Order"] = Relationship(back_populates="user_profile")
   product_reviews: List["ProductReview"] = Relationship(
      back_populates="user_profile", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
   )






