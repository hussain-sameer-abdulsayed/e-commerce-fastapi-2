from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
PhoneNumber.phone_format = 'E164'

from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID





class UserBase(BaseSchemaConfig):
   full_name: str
   

class UserCreate(UserBase):
   password: str = Field(min_length=6, max_length=100)
   phone_number: Optional[PhoneNumber] = None
   email: EmailStr


class UserUpdate(BaseSchemaConfig):
   full_name: Optional[str] = None


class UserRead(UserBase, BaseSchema):
   user_name: str
   phone_number: str
   email: str



