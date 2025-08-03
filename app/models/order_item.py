from __future__ import annotations
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4, UUID

if TYPE_CHECKING:
   from app.models.product import Product
   from app.models.order import Order


class OrderItemBase(SQLModel, table=False):
   quantity: int
   unit_price: Decimal
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: Optional[datetime] = None

   product_id: UUID = Field(foreign_key="products.id")
   
   order_id: Optional[UUID] = Field(default=None, foreign_key="orders.id", index=True)
   
   @property
   def sub_total(self) -> Decimal:
      return self.unit_price * self.quantity



class OrderItem(OrderItemBase, table=True):
   __tablename__ = "order_items"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   product: "Product" = Relationship(back_populates="order_items")
   order: Optional["Order"] = Relationship(back_populates="order_items")




