from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from .base_schema import BaseSchemaConfig, BaseSchema, DiscountBase, DiscountUpdate


class CategoryDiscountBase(BaseSchemaConfig):
   category_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class CategoryDiscountCreate(DiscountBase):
   pass


class CategoryDiscountUpdate(DiscountUpdate):
   pass

class CategoryDiscountRead(CategoryDiscountBase, BaseSchema):
   is_currently_active: bool



