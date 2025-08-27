
from datetime import date
from sqlmodel import Relationship, Field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple
from uuid import uuid4
from app.authentication.auth_schema import UserRole

from app.models.base_model import BaseModel


if TYPE_CHECKING:
   from app.models import SellerProfile, Address, CouponUsage, Cart, UserProfile, Category

def generate_user_name(full_name: str) -> str:
    clean_name = "".join(full_name.split()).lower()

    unique_number = str(uuid4().int)[-6:]

    return f"{clean_name}{unique_number}"

class UserBase(BaseModel, table=False):
   user_name: str = Field(default=None, index=True, unique=True)
   full_name: str
   phone_number: Optional[str] = None
   email: str
   password_hash: str
   is_active: bool = Field(default=True)
   is_verified: bool = Field(default=False)
   role: UserRole = Field(default= UserRole.USER)
   refresh_token: Optional[str] = None



   def __init__(self, **data) -> None:
      super().__init__(**data)
      if not data.get("user_name") and self.full_name:
         self.user_name = generate_user_name(self.full_name)

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





