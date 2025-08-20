from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field, computed_field

from app.schemas.product import ProductRead
from .base_schema import BaseSchemaConfig, BaseSchema


class CartItemBase(BaseSchemaConfig):
   quantity: int = Field(gt=0, le=999, description="Quantity must be between 1 and 999")
   product_id: UUID

class CartItemCreate(CartItemBase):
   pass


class CartItemUpdate(BaseSchemaConfig):
   quantity: int = Field(gt=0, le=999, description="Quantity must be between 1 and 999")


class CartItemRead(CartItemBase, BaseSchema):
   cart_id: UUID
   unit_price: Decimal = Field(ge=0, description="Unit price must be non-negative")

   @computed_field
   @property
   def total(self) -> Decimal:
      return self.unit_price * self.quantity


class CartItemWithProduct(CartItemRead):
   product: ProductRead


try:
   from .product import ProductRead
   CartItemWithProduct.model_rebuild()
except ImportError:
   pass