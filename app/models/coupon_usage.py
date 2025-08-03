from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID



if TYPE_CHECKING:
   from app.models.coupon import Coupon
   from app.models.user import User



class CouponUsageBase(SQLModel, table=False):
   __tablename__ = "coupon_usages"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
   used_at: datetime = Field(default_factory=datetime.utcnow)


   user_id: UUID = Field(foreign_key="users.id", index=True)
   


   coupon_id: UUID = Field(foreign_key="coupons.id", index=True)
   



class CouponUsage(CouponUsageBase, table=True):
   __tablename__ = "coupon_usages"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   coupon: "Coupon" = Relationship(back_populates="coupon_usages")
   user: "User" = Relationship(back_populates="coupon_usages")

