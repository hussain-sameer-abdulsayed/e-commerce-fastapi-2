from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID
from app.enums.enums import Gender



class UserProfileBase(BaseSchemaConfig):
   bio: str
   gender: Gender = Gender.MALE
   birth_date: date

class UserProfileCreate(UserProfileBase):
   user_id: UUID

class UserProfileUpdate(BaseSchemaConfig):
   bio: Optional[str] = None
   gender: Optional[Gender] = None 
   birth_date: Optional[date] = None

class UserProfileRead(UserProfileBase, BaseSchema):
   user_id: UUID
   images: List["ImageRead"] = []

   @property
   def main_iamge_url(self) -> Optional[str]:
      return self.images[0].file_path if self.images else None
   

try:
   from .image import ImageRead
   UserProfileRead.model_rebuild()
except ImportError:
   pass


