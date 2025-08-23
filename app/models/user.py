
from sqlmodel import Relationship, Field
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from app.models.base_model import BaseModel


if TYPE_CHECKING:
   from app.models import SellerProfile, Address, CouponUsage, Cart, UserProfile, Category


class UserBase(BaseModel, table=False):
   user_name: str = Field(default_factory=lambda: str(uuid4()),index=True, unique=True)
   full_name: str
   phone_number: Optional[str] = None
   email: str
   password_hash: str



class User(UserBase, table=True):
   __tablename__ = "users" # type: ignore

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





