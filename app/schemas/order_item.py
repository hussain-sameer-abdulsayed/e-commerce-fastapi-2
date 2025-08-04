from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional
from .base_schema import BaseSchema
from uuid import UUID


class OrderItemBase(BaseSchema):
   product_id: UUID
   quantity: int
   

class OrderItemCreate(OrderItemBase):
   pass

class OrderItemUpdate(OrderItemBase):
   quantity: Optional[int] = None


class OrderItemRead(OrderItemBase):
   id: UUID
   order_id: UUID
   unit_price: Decimal
   created_at: datetime
   updated_at: Optional[datetime] = None
   sub_total: Decimal

