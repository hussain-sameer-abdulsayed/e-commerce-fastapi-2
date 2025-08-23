from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserCreate, UserUpdate


class UserService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = UserRepository(db)


   async def get_all(self) -> List[UserRead]:
      users = await self.repository.get_all()
      return [UserRead.model_validate(user) for user in users]


   async def get_by_id(self, id: UUID) -> Optional[UserRead]:
      user = await self.repository.get_by_id(id)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      return UserRead.model_validate(user)


   async def get_by_email(self, email: str) -> Optional[UserRead]:
      user = await self.repository.get_by_email(email)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      return UserRead.model_validate(user)
   

   async def get_by_username(self, username: UUID) -> Optional[UserRead]:
      user = await self.repository.get_by_username(username)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      return UserRead.model_validate(user)


   async def get_by_phone(self, phone: str) -> Optional[UserRead]:
      user = await self.repository.get_by_phone(phone)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      return UserRead.model_validate(user)


   async def get_with_profiles(self, user_id: UUID) -> Optional[UserRead]:
      user = await self.repository.get_with_profiles(user_id)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      return UserRead.model_validate(user)


   async def updated(self, user_id: UUID, update_data: UserUpdate) -> UserRead:
      user = await self.repository.get_by_id(user_id)
      if not user:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
         )
      
      update_dict = update_data.model_dump(exclude_unset= True)

      for field, value in update_dict.items():
         if hasattr(user, field) and value is not None:
            setattr(user, field, value)

      updated_user = await self.repository.update(user)

      return UserRead.model_validate(updated_user)


   async def delete(self, user_id: UUID) -> bool:
      result = await self.repository.delete(user_id)
      if not result:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
      return result



