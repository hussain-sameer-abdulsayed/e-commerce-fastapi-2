from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from .base_schema import BaseSchema


class CategoryDiscountBase(BaseSchema):
   category_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: date
   end_at: date


class CategoryDiscountCreate(CategoryDiscountBase):
   pass


class CategoryDiscountUpdate(BaseSchema):
   category_id: Optional[UUID] = None
   discount_amount: Optional[int] = None
   is_active: Optional[bool] = None
   start_at: Optional[date] = None
   end_at: Optional[date] = None


class CategoryDiscountRead(CategoryDiscountBase):
   id: UUID
   created_at: datetime
   updated_at: datetime
   is_currently_active: bool


