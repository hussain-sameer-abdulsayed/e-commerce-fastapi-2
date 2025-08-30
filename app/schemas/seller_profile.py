from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber
PhoneNumber.phone_format = 'E164'



class SellerProfileBase(BaseSchemaConfig):
   store_name: str
   store_description: str
   store_phone_number: PhoneNumber


class SellerProfileCreate(SellerProfileBase):
   user_id: UUID ## remove this, the user_id came with token



class SellerProfileUpdate(BaseSchemaConfig):
   store_name: Optional[str] = None
   store_description: Optional[str] = None
   store_phone_number: Optional[str] = None


class SellerProfileRead(SellerProfileBase, BaseSchema):
   user_id: UUID
   is_verified: bool
   is_active: bool
   images: List["ImageRead"] = []

   @property
   def main_image_url(self) -> Optional[str]:
      return self.images[0].file_path if self.images else None


try:
   from app.schemas.image import ImageRead
   SellerProfileRead.model_rebuild()
except ImportError:
   pass

