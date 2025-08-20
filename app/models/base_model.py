from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime

def utc_now_naive() -> datetime:
    """Helper function to get current UTC time as naive datetime"""
    return datetime.utcnow()

class BaseModel(SQLModel, table=False):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    
    created_at: datetime = Field(default_factory=utc_now_naive)
    updated_at: datetime = Field(default_factory=utc_now_naive)