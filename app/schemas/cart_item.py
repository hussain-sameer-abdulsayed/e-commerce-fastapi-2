from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from .base_schema import BaseSchema


class CartItemBase(BaseSchema):
   quantity: int
   product_id: UUID

class CartItemCreate(CartItemBase):
   pass


class CartItemUpdate(BaseSchema):
   quantity: Optional[int] = None


class CartItemRead(CartItemBase):
   id: UUID
   cart_id: UUID
   unit_price: Decimal
   total: Decimal
   created_at: datetime
   updated_at: datetime

