
from datetime import datetime
from sqlmodel import Field

from app.models.base_model import BaseModel

class DiscountBase(BaseModel, table=False):
    discount_amount: int
    is_active: bool = Field(default=True, index=True)

    start_at: datetime
    end_at: datetime
    

    @property
    def is_currently_active(self) -> bool:
        now = datetime.now()
        return self.is_active and self.start_at <= now <= self.end_at
    

    