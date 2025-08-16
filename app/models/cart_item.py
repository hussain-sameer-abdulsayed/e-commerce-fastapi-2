
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import uuid4, UUID




if TYPE_CHECKING:
   from app.models import Cart, Product


class CartItemBase(SQLModel, table=False):
   quantity: int = Field(1, gt=0)
   unit_price: Decimal = Field(0, gt=0)
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: datetime = Field(default_factory=datetime.utcnow)


   cart_id: UUID = Field(foreign_key="carts.id", index=True)
   
   product_id: UUID = Field(foreign_key="products.id", index=True)
   

   @property
   def total(self) -> Decimal:
      return self.unit_price * self.quantity



class CartItem(CartItemBase, table=True):
   __tablename__ = "cart_items"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   cart: "Cart" =  Relationship(back_populates="cart_items")
   product: "Product" = Relationship(back_populates="cart_items")


