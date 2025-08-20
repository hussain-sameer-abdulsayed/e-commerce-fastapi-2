from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator
from .base_schema import BaseSchemaConfig, BaseSchema



class CouponBase(BaseSchemaConfig):
   discount_amount: int = Field(gt=0, lt=101)
   min_order_amount: Decimal
   max_uses: int
   start_at: datetime
   end_at: datetime
   is_active: bool = True


   @field_validator('end_at')
   @classmethod
   def validate_end_date(cls, v: datetime) -> datetime:
      """Validate that end date is today or in the future"""
      now = datetime.now()
      if v <= now:
         raise ValueError('End date must be today or in the future')
      return v
   

   @model_validator(mode='after')
   def validate_date_range(self):
      """Validate that end date is after start date"""
      if self.end_at <= self.start_at:
         raise ValueError('End date must be after start date')
      return self


class CouponCreate(CouponBase):
   pass


class CouponUpdate(BaseSchemaConfig):
   discount_amount: Optional[int] = Field(None, gt=0, lt=101)
   min_order_amount: Optional[Decimal] = None
   max_uses: Optional[int] = None
   start_at: Optional[datetime] = None
   end_at: Optional[datetime] = None


   @field_validator('end_at')
   @classmethod
   def validate_end_date_update(cls, v: Optional[datetime] = None) -> Optional[datetime]:
      """Validate end date for updates (allow current date for active coupons)"""
      if v is None:
         return v
        
      now = datetime.now()
      if v <= now:
         raise ValueError('End date must be today or in the future')
      return v
   

   @model_validator(mode='after')
   def validate_date_range_update(self):
      """Validate date range for updates"""
      if self.start_at is not None and self.end_at is not None:
         if self.end_at <= self.start_at:
               raise ValueError('End date must be after start date')
      return self


class CouponSetStatus(BaseSchemaConfig):
   is_active: bool


class CouponRead(CouponBase, BaseSchema):
   code: UUID
   used_count: int
   is_currently_active: bool




