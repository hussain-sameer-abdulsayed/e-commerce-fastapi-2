from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID

if TYPE_CHECKING:
   from app.models.address import Address
   from app.models.user import User
   from app.models.product import Product

   

class SellerProfileBase(SQLModel, table=False):
   store_name: str
   store_description: str
   main_image_url: str
   store_phone_number: str
   is_verified: bool = Field(default=False)
   is_active: bool = Field(default=True)
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None

   user_id: UUID = Field(foreign_key="users.id", index=True)


class SellerProfile(SellerProfileBase, table=True):
   __tablename__ = "seller_profiles"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
   user: "User" = Relationship(back_populates="seller_profile")

   addresses: List["Address"] = Relationship(back_populates="seller_profile", cascade_delete=True)
   
   products: List["Product"] = Relationship(back_populates="seller_profile", cascade_delete=True)






