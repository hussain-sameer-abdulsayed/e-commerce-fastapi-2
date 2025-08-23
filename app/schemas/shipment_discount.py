from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema, DiscountBase, DiscountUpdate
from uuid import UUID


class ShipmentDiscountBase(BaseSchemaConfig):
   shipment_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class ShipmentDiscountCreate(DiscountBase):
   pass


class ShipmentDiscountUpdate(DiscountUpdate):
   pass


class ShipmentDiscountRead(ShipmentDiscountBase, BaseSchema):
   is_currently_active: bool