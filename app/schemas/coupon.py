from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from .base_schema import BaseSchema



class CouponBase(BaseSchema):
   discount_amount: int
   min_order_amount: Decimal
   max_uses: int
   start_at: date
   end_at: date
   is_active: bool = True


class CouponCreate(CouponBase):
   pass


class CouponUpdate(BaseSchema):
   discount_amount: Optional[int] = None
   min_order_amount: Optional[Decimal] = None
   max_uses: Optional[int] = None
   start_at: datetime
   end_at: datetime
   is_active: Optional[bool] = None


class CouponRead(CouponBase):
   id: UUID
   code: str
   used_count: int
   is_currently_active: bool
   created_at: datetime
   updated_at: datetime
   # coupon_usages = Optional[List["CouponUsageRead"]] = None



# from .coupon_usage import CouponUsageRead
# CouponRead.model_rebuild()