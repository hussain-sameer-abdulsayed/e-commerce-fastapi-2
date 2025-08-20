from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID




class SellerProfileBase(BaseSchemaConfig):
   store_name: str
   store_description: str
   main_image_url: str
   store_phone_number: str


class SellerProfileCreate(SellerProfileBase):
   user_id: UUID



class SellerProfileUpdate(BaseSchemaConfig):
   store_name: Optional[str] = None
   store_description: Optional[str] = None
   main_image_url: Optional[str] = None
   store_phone_number: Optional[str] = None


class SellerProfileRead(SellerProfileBase, BaseSchema):
   user_id: UUID
   is_verified: bool
   is_active: bool




