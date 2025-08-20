from __future__ import annotations
from fastapi import UploadFile
from typing import List, Optional
from uuid import UUID
from .base_schema import BaseSchemaConfig, BaseSchema



class CategoryBase(BaseSchemaConfig):
   name: str 
   description: str
   main_image_url: Optional[str] = None
   


class CategoryCreate(CategoryBase):
   created_by_id : UUID


class CategoryUpdate(BaseSchemaConfig):
   name: Optional[str] = None
   description: Optional[str] = None
   main_image_url: Optional[str] = None


class CategoryRead(CategoryBase, BaseSchema):
   created_by_id : UUID
   

class CategoryWithProducts(CategoryRead):
   products: Optional[List["ProductRead"]] = None


try:
   from .product import ProductRead
   CategoryWithProducts.model_rebuild()
except ImportError:
   pass