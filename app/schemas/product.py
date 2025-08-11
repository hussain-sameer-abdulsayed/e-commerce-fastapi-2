from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


from .base_schema import BaseSchema
from uuid import UUID



class ProductBase(BaseSchema):
   name: str
   price: Decimal
   stock_quantity: int = 0
   description: str
   main_image_url: str
   # seller_profile_id: Optional[UUID] = None

class ProductCreate(ProductBase):
   category_ids: List[UUID]
   seller_profile_id: UUID


class ProductUpdate(BaseSchema):
   name: Optional[str] = None
   price: Optional[Decimal] = None
   stock_quantity: Optional[int] = None
   description: Optional[str] = None
   main_image_url: Optional[str] = None
   category_ids: Optional[List[UUID]] = None



class ProductRead(ProductBase):
   id: UUID
   seller_profile_id: UUID
   created_at: datetime
   updated_at: datetime
   is_available: bool


class ProductWithCategories(ProductRead):
   categories: List[CategoryRead]

      
try:
   from app.schemas.category import CategoryRead
   ProductWithCategories.model_rebuild()
except ImportError:
   pass