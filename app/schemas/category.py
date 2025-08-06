from __future__ import annotations
from fastapi import UploadFile
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from .base_schema import BaseSchema



class CategoryBase(BaseSchema):
   name: str 
   description: str
   main_image_url: Optional[str] = None
   


class CategoryCreate(CategoryBase):
   created_by_id : UUID


class CategoryUpdate(CategoryBase):
   name: Optional[str] = None
   description: Optional[str] = None
   main_image_url: Optional[str] = None


class CategoryRead(CategoryBase):
   id: UUID
   created_by_id : UUID
   created_at: datetime 
   updated_at : Optional[datetime] = None
   products: Optional[List["ProductRead"]] = None
   


from .product import ProductRead
CategoryRead.model_rebuild()