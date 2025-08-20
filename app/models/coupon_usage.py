
from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from app.models.base_model import utc_now_naive


if TYPE_CHECKING:
   from app.models import Coupon, User



class CouponUsageBase(SQLModel, table=False):
   used_at: datetime = Field(default_factory= utc_now_naive)

   user_id: UUID = Field(foreign_key="users.id", index=True)
   coupon_id: UUID = Field(foreign_key="coupons.id", index=True)
   


class CouponUsage(CouponUsageBase, table=True):
   __tablename__ = "coupon_usages" # type: ignore
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   coupon: "Coupon" = Relationship(back_populates="coupon_usages")
   user: "User" = Relationship(back_populates="coupon_usages")

