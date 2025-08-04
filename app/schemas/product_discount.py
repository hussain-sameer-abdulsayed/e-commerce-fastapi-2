from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from .base_schema import BaseSchema
from uuid import UUID


class ProductDiscountBase(BaseSchema):
   product_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: date
   end_at: date


class ProductDiscountCreate(ProductDiscountBase):
   pass


class ProductDiscountUpdate(ProductDiscountBase):
   discount_amount: Optional[int] = None
   is_active: Optional[bool] = None
   start_at: Optional[datetime] = None
   end_at: Optional[datetime] = None


class ProductDiscountRead(ProductDiscountBase):
   id: UUID
   created_at: datetime
   updated_at: Optional[datetime] = None
   is_currently_active: bool


