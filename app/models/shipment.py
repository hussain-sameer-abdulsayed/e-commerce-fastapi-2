
from decimal import Decimal
from sqlmodel import Relationship, Field
from typing import TYPE_CHECKING, List

from app.enums.enums import Province
from app.models.base_model import BaseModel


if TYPE_CHECKING:
   from app.models import ShipmentDiscount, Order


class ShipmentBase(BaseModel, table=False):
   province: Province = Field(default=Province.BAGHDAD)
   cost: Decimal = Field(ge=0.00, le=25000.00)



class Shipment(ShipmentBase, table=True):
   __tablename__ = "shipments" # type: ignore

   orders: List["Order"] = Relationship(back_populates="shipment")
   shipment_discounts: List["ShipmentDiscount"] = Relationship(
      back_populates="shipment", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
   )






