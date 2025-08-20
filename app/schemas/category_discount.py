from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from .base_schema import BaseSchemaConfig, BaseSchema


class CategoryDiscountBase(BaseSchemaConfig):
   category_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class CategoryDiscountCreate(CategoryDiscountBase):
   pass


class CategoryDiscountUpdate(BaseSchemaConfig):
   category_id: Optional[UUID] = None
   discount_amount: Optional[int] = None
   is_active: Optional[bool] = None
   start_at: Optional[datetime] = None
   end_at: Optional[datetime] = None


class CategoryDiscountRead(CategoryDiscountBase, BaseSchema):
   is_currently_active: bool



