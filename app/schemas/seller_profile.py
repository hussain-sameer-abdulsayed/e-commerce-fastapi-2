from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber
PhoneNumber.phone_format = 'E164'



class SellerProfileBase(BaseSchemaConfig):
   store_name: str
   store_description: str
   main_image_url: str
   store_phone_number: PhoneNumber


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




