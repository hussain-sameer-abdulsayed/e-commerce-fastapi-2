from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, computed_field

from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID



class ProductBase(BaseSchemaConfig):
   name: str
   price: Decimal = Field(gt=0.00)
   stock_quantity: int = Field(default=0, ge=0)
   description: str
   main_image_url: str
   # seller_profile_id: Optional[UUID] = None

class ProductCreate(ProductBase):
   category_ids: List[UUID]
   seller_profile_id: UUID


class ProductUpdate(BaseSchemaConfig):
   name: Optional[str] = None
   price: Optional[Decimal] = Field(None, gt=0.00)
   stock_quantity: Optional[int] = Field(None, ge=0)
   description: Optional[str] = None
   main_image_url: Optional[str] = None
   category_ids: Optional[List[UUID]] = None



class ProductRead(ProductBase, BaseSchema):
   seller_profile_id: UUID

   @computed_field
   @property
   def is_available(self) -> bool:
      return self.stock_quantity > 0
   


class ProductWithCategories(ProductRead):
   categories: List[CategoryRead]

      
try:
   from app.schemas.category import CategoryRead
   ProductWithCategories.model_rebuild()
except ImportError:
   pass