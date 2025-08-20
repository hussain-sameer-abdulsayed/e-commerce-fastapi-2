from __future__ import annotations
from datetime import datetime
from uuid import UUID
from .base_schema import BaseSchemaConfig


class CouponUsageBase(BaseSchemaConfig):
   user_id: UUID
   coupon_id: UUID


class CouponUsageCreate(CouponUsageBase):
   pass


class CouponUsageRead(CouponUsageBase):
   id: UUID
   used_at: datetime


   class Config:
        from_attributes = True
        arbitrary_types_allowed = True
