
from decimal import Decimal
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from uuid import uuid4, UUID

from app.enums.enums import Province


if TYPE_CHECKING:
   from app.models import ShipmentDiscount, Order


class ShipmentBase(SQLModel, table=False):
   province: Province = Field(default=Province.BAGHDAD)
   cost: Decimal = Field(gt=0)
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: datetime = Field(default_factory=datetime.utcnow)



class Shipment(ShipmentBase, table=True):
   __tablename__ = "shipments"
   id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

   orders: List["Order"] = Relationship(back_populates="shipment")
   shipment_discounts: List["ShipmentDiscount"] = Relationship(
      back_populates="shipment", 
      cascade_delete=True,
      sa_relationship_kwargs={'lazy': 'selectin'}
   )






