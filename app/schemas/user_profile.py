from __future__ import annotations
from datetime import date, datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID
from app.enums.enums import Gender



class UserProfileBase(BaseSchemaConfig):
   main_image_url: str
   bio: str
   gender: Gender = Gender.MALE
   birth_date: date

   

class UserProfileCreate(UserProfileBase):
   user_id: UUID


class UserProfileUpdate(BaseSchemaConfig):
   main_image_url: Optional[str] = None
   bio: Optional[str] = None
   gender: Optional[Gender] = None 
   birth_date: Optional[date] = None



class UserProfileRead(UserProfileBase, BaseSchema):
   user_id: UUID
   


