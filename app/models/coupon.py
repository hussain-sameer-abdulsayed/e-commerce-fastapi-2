from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models import Cart, CouponUsage, Order


class CouponBase(BaseModel, table=False):
    code: UUID = Field(default_factory=uuid4, index=True, unique=True)
    discount_amount: int
    min_order_amount: Decimal
    max_uses: int
    used_count: int = Field(default=0)

    start_at: datetime
    end_at: datetime

    is_active: bool = Field(default=True, index=True)

    @property
    def is_currently_active(self) -> bool:
        now = datetime.now()
        return (
            self.is_active
            and self.used_count < self.max_uses
            and self.start_at <= now <= self.end_at
        )

class Coupon(CouponBase, table=True):
    __tablename__ = "coupons" # type: ignore

    coupon_usages: List["CouponUsage"] = Relationship(
        back_populates="coupon",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    orders: List["Order"] = Relationship(back_populates="coupon")
    carts: List["Cart"] = Relationship(back_populates="coupon")
