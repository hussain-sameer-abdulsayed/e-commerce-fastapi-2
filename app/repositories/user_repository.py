from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.models.user import User



class UserRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_all(self) -> List[User]:
      statement = select(User).order_by(User.user_name)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[User]:
      statement = select(User).where(User.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
 
 
   async def get_by_email(self, email: str) -> Optional[User]:
      statement = select(User).where(User.email == email)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_username(self, username: UUID) -> Optional[User]:
      statement = select(User).where(User.user_name == username)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_phone(self, phone: str) -> Optional[User]:
      statement = select(User).where(User.phone_number == phone)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()

   
   async def get_with_profiles(self, user_id: UUID) -> Optional[User]:
      statement = (
         select(User)
         .options(
            selectinload(User.user_profile),
            selectinload(User.seller_profile)
         )
         .where(User.id == user_id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def create(self, user: User) -> User:
      self.db.add(user)
      await self.db.commit()
      await self.db.refresh(user)
      return user


   async def update(self, user: User) -> User:
      user.updated_at = datetime.utcnow()
      self.db.add(user)
      await self.db.commit()
      await self.db.refresh(user)
      return user


   async def delete(self, id: UUID) -> bool:
      user = await self.get_by_id(id)
      if not user:
         return False
      await self.db.delete(user)
      await self.db.commit()
      return True


   async def exists_by_phone(self, phone: str, exclude_id: Optional[UUID] = None) -> bool:
      statement = select(User).where(User.phone_number == phone)
      if exclude_id:
         statement = statement.where(User.id != exclude_id)

      result = await self.db.execute(statement)
      user = result.first()
      return user is not None


   async def exists_by_email(self, email: str, exclude_id: Optional[UUID] = None) -> bool:
      statement = select(User).where(User.email == email)
      if exclude_id:
         statement = statement.where(User.id != exclude_id)

      result = await self.db.execute(statement)
      user = result.first()
      return user is not None


