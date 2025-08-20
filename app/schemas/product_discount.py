from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID


class ProductDiscountBase(BaseSchemaConfig):
   product_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class ProductDiscountCreate(ProductDiscountBase):
   pass


class ProductDiscountUpdate(BaseSchemaConfig):
   discount_amount: Optional[int] = None
   is_active: Optional[bool] = None
   start_at: datetime
   end_at: datetime


class ProductDiscountRead(ProductDiscountBase, BaseSchema):
   is_currently_active: bool


