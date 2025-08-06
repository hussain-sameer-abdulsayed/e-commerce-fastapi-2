
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from uuid import UUID
from app.models.discount_base import DiscountBase

if TYPE_CHECKING:
   from app.models import Product


class ProductDiscount(DiscountBase, table=True):
   __tablename__ = "product_discounts"
   product_id: UUID = Field(foreign_key="products.id", index=True)
   product : "Product" = Relationship(back_populates="product_discounts")



