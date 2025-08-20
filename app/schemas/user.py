from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID





class UserBase(BaseSchemaConfig):
   full_name: str
   

class UserCreate(UserBase):
   password: str = Field(min_length=6, max_length=100)
   phone_number: str = Field(max_length=14, min_length=11)
   email: str


class UserUpdate(BaseSchemaConfig):
   full_name: Optional[str] = None


class UserRead(UserBase, BaseSchema):
   user_name: str
   phone_number: str
   email: str



