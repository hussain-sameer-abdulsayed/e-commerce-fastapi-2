
from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4, UUID


if TYPE_CHECKING:
   from app.models import SellerProfile, Address, CouponUsage, Cart, UserProfile, Category


class UserBase(SQLModel, table=False):
   user_name: str = Field(default_factory=lambda: str(uuid4()),index=True, unique=True)
   full_name: str
   phone_number: str
   email: str = Field(index=True)
   password_hash: str
   
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None





class User(UserBase, table=True):
   __tablename__ = "users"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   addresses: List["Address"] = Relationship(
      back_populates="user", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
      )
   coupon_usages: List["CouponUsage"] = Relationship(back_populates="user", cascade_delete=True)
   cart: Optional["Cart"] = Relationship(back_populates="user", cascade_delete=True)
   seller_profile: Optional["SellerProfile"] = Relationship(back_populates="user", cascade_delete=True)
   user_profile: Optional["UserProfile"] = Relationship(back_populates="user", cascade_delete=True)
   categories: List["Category"] = Relationship(back_populates="user")





