
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import uuid4, UUID

class DiscountBase(SQLModel, table=False):  # Keep table=False for base class
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    discount_amount: int
    is_active: bool = Field(default=True, index=True)
    start_at: date
    end_at: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def is_currently_active(self) -> bool:
        now = datetime.utcnow().date()  # Convert to date for comparison
        return self.is_active and self.start_at <= now <= self.end_at
    

    