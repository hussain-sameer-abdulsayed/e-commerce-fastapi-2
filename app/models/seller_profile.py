
from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship
from uuid import UUID

from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import Address, User, Product

   

class SellerProfileBase(BaseModel, table=False):
   store_name: str
   store_description: str
   main_image_url: str
   store_phone_number: str
   is_verified: bool = Field(default=False)
   is_active: bool = Field(default=True)

   user_id: UUID = Field(foreign_key="users.id", index=True)


class SellerProfile(SellerProfileBase, table=True):
   __tablename__ = "seller_profiles" # type: ignore
   
   user: "User" = Relationship(back_populates="seller_profile")

   addresses: List["Address"] = Relationship(
      back_populates="seller_profile", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
      )
   
   products: List["Product"] = Relationship(
      back_populates="seller_profile",
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
      )






