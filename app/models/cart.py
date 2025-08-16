
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4, UUID



if TYPE_CHECKING:
      from app.models import CartItem, User, Coupon



class CartBase(SQLModel, table=False):
   total: Optional[Decimal] = Decimal("0.00")
   coupon_amount:  Optional[Decimal] = Decimal("0.00")
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: datetime = Field(default_factory=datetime.utcnow)

   user_id: UUID = Field(foreign_key="users.id", index=True, unique=True)
   coupon_id: Optional[UUID] = Field(default=None, foreign_key="coupons.id")

class Cart(CartBase, table=True):
   __tablename__ = "carts"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   cart_items: List["CartItem"] = Relationship(
       back_populates="cart", 
       cascade_delete=True,
       sa_relationship_kwargs={'lazy': 'selectin'}
       )
   coupon: Optional["Coupon"] = Relationship(back_populates="carts")
   user: "User" = Relationship(back_populates="cart")



