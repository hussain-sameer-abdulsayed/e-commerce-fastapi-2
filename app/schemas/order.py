from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from app.enums.enums import Order_Status
from .base_schema import BaseSchema




class OrderBase(BaseSchema):
   address_id: UUID
   ship_to_province: str
   ship_to_city: str
   ship_to_street: str
   ship_to_contact: str
   shipment_id: UUID


class OrderCreate(OrderBase):
   user_profile_id : UUID
   coupon_id: Optional[UUID] = None
   status: Optional[Order_Status] = Order_Status.PENDING


class OrderUpdate(OrderBase):
    address_id: Optional[UUID] = None
    ship_to_province: Optional[str] = None
    ship_to_city: Optional[str] = None
    ship_to_street: Optional[str] = None
    ship_to_contact: Optional[str] = None
    shipment_id: Optional[UUID] = None


class OrderRead(OrderBase):
    id: UUID
    user_profile_id: UUID
    order_number: str
    coupon_id: Optional[UUID] = None
    coupon_amount: Optional[Decimal] = None
    sub_total: Decimal
    shipping_cost: Decimal
    total: Decimal
    order_items: List["OrderItemRead"]
    status: Order_Status
    created_at: datetime
    updated_at: Optional[datetime] = None




from .order_item import OrderItemRead
OrderRead.model_rebuild()