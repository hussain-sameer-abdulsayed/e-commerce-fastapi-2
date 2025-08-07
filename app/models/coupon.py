
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4, UUID

if TYPE_CHECKING:
   from app.models import Cart, CouponUsage, Order


class CouponBase(SQLModel, table=False):
   code: str = Field(default_factory=lambda: str(uuid4()), index=True, unique=True)
   discount_amount: int
   min_order_amount: Decimal
   max_uses: int
   used_count: int = Field(default=0)
   start_at: datetime = Field(index=True)
   end_at: datetime = Field(index=True)
   is_active: bool = Field(default=True, index=True)
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None

   @property
   def is_currently_active(self) -> bool:
      now = datetime.utcnow()  # Keep as datetime
      return (self.is_active and 
               self.used_count < self.max_uses and 
               self.start_at <= now <= self.end_at)


class Coupon(CouponBase, table=True):
   __tablename__ = "coupons"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   coupon_usages: List["CouponUsage"] = Relationship(
      back_populates="coupon", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
      )
   
   orders: List["Order"] = Relationship(back_populates="coupon")

   carts: List["Cart"] = Relationship(back_populates="coupon")




