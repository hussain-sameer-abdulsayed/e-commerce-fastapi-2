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

class ProductCreate(ProductBase):
   category_ids: List[UUID]


class ProductUpdate(BaseSchemaConfig):
   name: Optional[str] = None
   price: Optional[Decimal] = Field(None, gt=0.00)
   stock_quantity: Optional[int] = Field(None, ge=0)
   description: Optional[str] = None
   category_ids: Optional[List[UUID]] = None



class ProductRead(ProductBase, BaseSchema):
   seller_profile_id: UUID
   images: List["ImageRead"] = []

   @computed_field
   @property
   def is_available(self) -> bool:
      return self.stock_quantity > 0
   
   @property
   def main_image_url(self) -> Optional[str]:
      return self.images[0].file_path if self.images else None

class ProductWithCategories(ProductRead):
   categories: List[CategoryRead] = []

      
try:
   from app.schemas.category import CategoryRead
   from .image import ImageRead
   ProductWithCategories.model_rebuild()
except ImportError:
   pass