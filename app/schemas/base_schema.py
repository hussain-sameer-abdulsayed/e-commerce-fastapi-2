from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal

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




    