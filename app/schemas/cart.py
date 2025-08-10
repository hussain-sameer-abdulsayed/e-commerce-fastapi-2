from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from .base_schema import BaseSchema



class CartBase(BaseSchema):
   user_id: UUID


class CartCreate(CartBase):
   pass


class CartRead(CartBase):
   id: UUID
   total: Optional[Decimal] = None
   coupon_id: Optional[UUID] = None
   coupon_amount: Optional[Decimal]  = None
   created_at: datetime
   updated_at: datetime


class CartWithItems(CartRead):
   cart_items: Optional[List["CartItemRead"]] = None


try:
   from .cart_item import CartItemRead
   CartWithItems.model_rebuild()
except ImportError:
   pass