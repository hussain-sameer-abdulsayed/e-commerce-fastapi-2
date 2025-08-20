
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from datetime import date
from uuid import uuid4, UUID
from app.enums.enums import Order_Status
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models import Coupon, Shipment, UserProfile, Address, OrderItem


def generate_order_number() -> str:
    today = date.today()
    # Generate a 6-digit number from UUID (more unique than random)
    unique_number = str(uuid4())[-6:].zfill(6)
    return f"{today.year}-{today.month}-{today.day}-{unique_number}"


class OrderBase(BaseModel, table=False):
   order_number: str = Field(default_factory=generate_order_number, index=True, unique=True)
   ship_to_province: str
   ship_to_city: str
   ship_to_street: str
   ship_to_contact: str
   coupon_amount: Optional[Decimal] = Decimal("0.00")
   sub_total: Decimal
   shipping_cost: Decimal
   total: Decimal
   status: Order_Status = Field(default=Order_Status.PENDING)

   coupon_id: Optional[UUID] = Field(default=None, foreign_key="coupons.id")
   shipment_id: UUID = Field(foreign_key="shipments.id")
   user_profile_id: UUID = Field(foreign_key="user_profiles.id", index=True)
   address_id: UUID = Field(foreign_key="addresses.id")

   @property
   def set_total(self) -> Decimal:
       if self.coupon_amount:
           return self.sub_total + self.shipping_cost - self.coupon_amount
       return self.sub_total + self.shipping_cost


class Order(OrderBase, table=True):
    __tablename__ = "orders" # type: ignore
    
    address: "Address" = Relationship(back_populates="orders")
    user_profile: "UserProfile" = Relationship(back_populates="orders")
    coupon: Optional["Coupon"] = Relationship(back_populates="orders")
    shipment: "Shipment" = Relationship(back_populates="orders")      
    order_items: List["OrderItem"] = Relationship(
        back_populates="order", 
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
        )

   


