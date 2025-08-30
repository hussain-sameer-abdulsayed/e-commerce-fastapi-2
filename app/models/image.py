from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from sqlalchemy import Uuid, table
from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import Product, Category, SellerProfile, UserProfile

class ImageBase(BaseModel, table= False):
   file_name: str = Field(index = True)
   original_file_name: str
   file_size: int = Field(ge=0) # in bytes
   mime_type: str

   ## foreign keys ##
   product_id: Optional[UUID] = Field(default= None, foreign_key="products.id", index= True)
   category_id: Optional[UUID] = Field(default= None, foreign_key="categories.id", index= True)
   seller_profile_id: Optional[UUID] = Field(default= None, foreign_key="seller_profiles.id", index= True)
   user_profile_id: Optional[UUID] = Field(default= None, foreign_key="user_profiles.id", index= True)


class Image(ImageBase, table= True):
   __tablename__ = "images" # type: ignore

   product: Optional["Product"] = Relationship(back_populates="images")
   category: Optional["Category"] = Relationship(back_populates="images")
   seller_profile: Optional["SellerProfile"] = Relationship(back_populates="images")
   user_profile: Optional["UserProfile"] = Relationship(back_populates="images")


