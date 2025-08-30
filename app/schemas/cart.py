from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from .base_schema import BaseSchemaConfig, BaseSchema
from pydantic import computed_field


class CartBase(BaseSchemaConfig):
   user_id: UUID


class CartCreate(CartBase):
   pass


class CartRead(CartBase, BaseSchema):
   total: Optional[Decimal] = None
   coupon_id: Optional[UUID] = None
   coupon_amount: Optional[Decimal]  = None

   @computed_field
   @property
   def final_total(self) -> Decimal:
      base_total = self.total or Decimal('0.00')
      discount = self.coupon_amount or Decimal('0.00')
      return base_total - discount


class CartWithItems(CartRead):
   cart_items: List["CartItemWithProduct"] = []


try:
   from .cart_item import CartItemWithProduct
   CartWithItems.model_rebuild()
except ImportError:
   pass

