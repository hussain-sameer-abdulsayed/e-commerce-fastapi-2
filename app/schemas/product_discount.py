from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema, DiscountBase, DiscountUpdate
from uuid import UUID


class ProductDiscountBase(BaseSchemaConfig):
   product_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class ProductDiscountCreate(DiscountBase):
   pass


class ProductDiscountUpdate(DiscountUpdate):
   pass


class ProductDiscountRead(ProductDiscountBase, BaseSchema):
   is_currently_active: bool


