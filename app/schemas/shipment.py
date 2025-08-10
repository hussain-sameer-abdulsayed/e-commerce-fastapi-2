from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from .base_schema import BaseSchema
from uuid import UUID
from app.enums.enums import Province



class ShipmentBase(BaseSchema):
   province: Province
   cost: Decimal 
   

class ShipmentCreate(ShipmentBase):
   pass


class ShipmentUpdate(BaseSchema):
   province: Optional[Province] = None
   cost: Optional[Decimal] = None 


class ShipmentRead(ShipmentBase):
   id: UUID
   province: Province
   cost: Decimal 
   created_at: datetime
   updated_at: datetime
   #shipment_discounts: Optional[List["ShipmentDiscountRead"]] = None



# from .shipment_discount import ShipmentDiscountRead
# ShipmentRead.model_rebuild()