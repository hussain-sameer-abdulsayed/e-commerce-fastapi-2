from __future__ import annotations
from decimal import Decimal
from typing import Optional

from pydantic import Field
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID
from app.enums.enums import Province



class ShipmentBase(BaseSchemaConfig):
   province: Province
   cost: Decimal = Field(ge=0.00, le=25000.00)
   

class ShipmentCreate(ShipmentBase):
   pass


class ShipmentUpdate(BaseSchemaConfig):
   province: Optional[Province] = None
   cost: Optional[Decimal] = Field(None, ge=0.00, le=25000.00)


class ShipmentRead(ShipmentBase, BaseSchema):
   province: Province

