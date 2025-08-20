from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID


class OrderItemBase(BaseSchemaConfig):
   product_id: UUID
   quantity: int = Field(1, ge=1, le=999)
   

class OrderItemCreate(OrderItemBase):
   pass

class OrderItemUpdate(BaseSchemaConfig):
   quantity: Optional[int] = None


class OrderItemRead(OrderItemBase, BaseSchema):
   order_id: UUID
   unit_price: Decimal
   sub_total: Decimal

