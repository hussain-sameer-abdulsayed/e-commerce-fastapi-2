from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models.user_profile import UserProfile





class UserProfileRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_all(self) -> List[UserProfile]:
      statement = select(UserProfile)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[UserProfile]:
      statement = select(UserProfile).where(UserProfile.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
      statement = select(UserProfile).where(UserProfile.user_id == user_id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_with_user(self, id: UUID) -> Optional[UserProfile]:
      statement = (
         select(UserProfile)
         .options(
            selectinload(UserProfile.user)
         )
         .where(UserProfile.id == id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def create(self, profile: UserProfile) -> UserProfile:
      self.db.add(profile)
      await self.db.commit()
      await self.db.refresh(profile)
      return profile


   async def update(self, profile: UserProfile) -> UserProfile:
      profile.updated_at = datetime.utcnow()
      self.db.add(profile)
      await self.db.commit()
      await self.db.refresh(profile)
      return profile


   async def delete(self, id: UUID) -> bool:
      profile = await self.get_by_id(id)
      if not profile:
         return False
      await self.db.delete(profile)
      await self.db.commit()
      return True
   


