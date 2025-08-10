from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from .base_schema import BaseSchema
from uuid import UUID





class UserBase(BaseSchema):
   full_name: str
   

class UserCreate(UserBase):
   password: str = Field(min_length=6)
   phone_number: str
   email: str


class UserUpdate(BaseSchema):
   full_name: Optional[str] = None


class UserRead(UserBase):
   id: UUID
   user_name: str
   created_at: datetime
   updated_at: datetime
   phone_number: str
   email: str
   #addresses: Optional[List["AddressRead"]] = None



# from .address import AddressRead
# UserRead.model_rebuild()
