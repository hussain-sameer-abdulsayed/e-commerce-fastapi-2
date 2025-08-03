from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4, UUID
from sqlmodel import Field, Relationship
from app.models.discount_base import DiscountBase


if TYPE_CHECKING:
   from app.models.shipment import Shipment


class ShipmentDiscount(DiscountBase, table=True):
   __tablename__ = "shipment_discounts"
   shipment_id: UUID = Field(foreign_key="shipments.id", index=True)
   shipment : "Shipment" = Relationship(back_populates="shipment_discounts")





