
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import Product, Order


class OrderItemBase(BaseModel, table=False):
   quantity: int
   unit_price: Decimal

   product_id: UUID = Field(foreign_key="products.id")
   
   order_id: Optional[UUID] = Field(default=None, foreign_key="orders.id", index=True)
   
   @property
   def sub_total(self) -> Decimal:
      return self.unit_price * self.quantity



class OrderItem(OrderItemBase, table=True):
   __tablename__ = "order_items" # type: ignore

   product: "Product" = Relationship(back_populates="order_items")
   order: Optional["Order"] = Relationship(back_populates="order_items")




