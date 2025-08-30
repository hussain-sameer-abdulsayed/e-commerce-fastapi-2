from __future__ import annotations
from fastapi import File ,UploadFile
from typing import List, Optional
from uuid import UUID

from .base_schema import BaseSchemaConfig, BaseSchema



class CategoryBase(BaseSchemaConfig):
   name: str 
   description: str
   
class CategoryCreate(CategoryBase):
   pass

class CategoryUpdate(BaseSchemaConfig):
   name: Optional[str] = None
   description: Optional[str] = None


class CategoryRead(CategoryBase, BaseSchema):
   created_by_id: UUID
   images: List["ImageRead"] = []

   @property
   def main_image_url(self) -> Optional[str]:
      return self.images[0].file_path if self.images else None
   

class CategoryWithProducts(CategoryRead):
   products: List["ProductRead"] = []


try:
   from .product import ProductRead
   from .image import ImageRead
   CategoryWithProducts.model_rebuild()
except ImportError:
   pass