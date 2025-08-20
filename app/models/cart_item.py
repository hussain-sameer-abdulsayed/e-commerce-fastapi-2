
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from uuid import UUID

from app.models.base_model import BaseModel

if TYPE_CHECKING:
   from app.models import Cart, Product


class CartItemBase(BaseModel, table=False):
   quantity: int = Field(1, gt=0)
   unit_price: Decimal = Field(0, gt=0)


   cart_id: UUID = Field(foreign_key="carts.id", index=True)
   
   product_id: UUID = Field(foreign_key="products.id", index=True)
   

   @property
   def total(self) -> Decimal:
      return self.unit_price * self.quantity



class CartItem(CartItemBase, table=True):
   __tablename__ = "cart_items" # type: ignore

   cart: "Cart" =  Relationship(back_populates="cart_items")
   product: "Product" = Relationship(back_populates="cart_items")


