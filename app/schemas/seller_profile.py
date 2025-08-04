from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from .base_schema import BaseSchema
from uuid import UUID




class SellerProfileBase(BaseSchema):
   store_name: str
   store_description: str
   main_image_url: str
   store_phone_number: str


class SellerProfileCreate(SellerProfileBase):
   user_id: UUID



class SellerProfileUpdate(SellerProfileBase):
   store_name: Optional[str] = None
   store_description: Optional[str] = None
   main_image_url: Optional[str] = None
   store_phone_number: Optional[str] = None


class SellerProfileRead(SellerProfileBase):
   id: UUID
   user_id: UUID
   is_verified: bool
   is_active: bool
   created_at: datetime
   updated_at: Optional[datetime]
   addresses: Optional[List["AddressRead"]] = None
   products: Optional[List["ProductRead"]] = None


from .address import AddressRead
from .product import ProductRead
SellerProfileRead.model_rebuild()


