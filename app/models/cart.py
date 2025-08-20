
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from app.models.base_model import BaseModel


if TYPE_CHECKING:
      from app.models import CartItem, User, Coupon



class CartBase(BaseModel, table=False):
   total: Optional[Decimal] = Decimal("0.00")
   coupon_amount:  Optional[Decimal] = Decimal("0.00")

   user_id: UUID = Field(foreign_key="users.id", index=True, unique=True)
   coupon_id: Optional[UUID] = Field(default=None, foreign_key="coupons.id")

class Cart(CartBase, table=True):
   __tablename__ = "carts" # type: ignore

   cart_items: List["CartItem"] = Relationship(
       back_populates="cart", 
       cascade_delete=True,
       sa_relationship_kwargs={'lazy': 'selectin'}
       )
   coupon: Optional["Coupon"] = Relationship(back_populates="carts")
   user: "User" = Relationship(back_populates="cart")



