from datetime import datetime
from typing import Optional
from uuid import UUID
from xml.dom.minidom import Entity
from pydantic import BaseModel
from decimal import Decimal

from app.enums.enums import Discount_Model_Type
from app.models import discount_base

class BaseSchemaConfig(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            Decimal: lambda x: float(round(x, 2)),
        }



class BaseSchema(BaseSchemaConfig):
    id: UUID
    created_at: datetime
    updated_at: datetime

class DiscountBase(BaseSchemaConfig):
    discount_type: Discount_Model_Type
    entity_id: UUID
    discount_amount: int
    is_active: bool = True
    start_at: datetime
    end_at: datetime

class DiscountUpdate(BaseSchemaConfig):
    discount_amount: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    
class DiscountSetStatus(BaseSchemaConfig):
    is_active: bool
    