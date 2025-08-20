from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID


class ShipmentDiscountBase(BaseSchemaConfig):
   shipment_id: UUID
   discount_amount: int
   is_active: bool = True
   start_at: datetime
   end_at: datetime


class ShipmentDiscountCreate(ShipmentDiscountBase):
   pass


class ShipmentDiscountUpdate(BaseSchemaConfig):
   shipment_id: Optional[UUID] = None
   discount_amount: Optional[int] = None
   is_active: Optional[bool] = None
   start_at: Optional[datetime] = None
   end_at: Optional[datetime] = None


class ShipmentDiscountRead(ShipmentDiscountBase, BaseSchema):
   is_currently_active: bool