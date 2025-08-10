from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchema
from uuid import UUID
from app.enums.enums import Gender



class UserProfileBase(BaseSchema):
   main_image_url: str
   bio: str
   gender: Gender = Gender.MALE
   birth_date: datetime

   

class UserProfileCreate(UserProfileBase):
   user_id: UUID


class UserProfileUpdate(BaseSchema):
   main_image_url: Optional[str] = None
   bio: Optional[str] = None
   gender: Optional[Gender] = None 
   birth_date: datetime



class UserProfileRead(UserProfileBase):
   id: UUID
   user_id: UUID
   created_at: datetime
   updated_at: datetime
   


