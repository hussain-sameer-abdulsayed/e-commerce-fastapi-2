
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.models.user import User
PhoneNumber.phone_format = 'E164'

from app.db.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.authentication.auth_dependency import (
   require_admin,
   require_user,
   get_current_active_user
)




router = APIRouter(
   responses={404: {"description" : "Not found"}}
)


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
   return UserService(db)


@router.get("/", response_model= List[UserRead], status_code= status.HTTP_200_OK)
async def get_all(
   service: UserService = Depends(get_user_service),
   current_user: User = Depends(require_admin)
):
   return await service.get_all()


@router.get("/with-profiles/{user_id}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def get_with_profiles(
   user_id: UUID,
   service: UserService = Depends(get_user_service)
):
   return await service.get_with_profiles(user_id)


@router.get("/email/{email}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def get_by_email(
   email: EmailStr,
   service: UserService = Depends(get_user_service)
):
   return await service.get_by_email(email)


@router.get("/username/{username}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def get_by_username(
   username: str,
   service: UserService = Depends(get_user_service)
):
   return await service.get_by_username(username)


@router.get("/phone/{phone}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def get_by_phone(
   phone: PhoneNumber,
   service: UserService = Depends(get_user_service)
):
   return await service.get_by_phone(str(phone))


@router.get("/{user_id}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def get_by_id(
   user_id: UUID,
   service: UserService = Depends(get_user_service)
):
   return await service.get_by_id(user_id)



@router.put("/{user_id}", response_model= UserRead, status_code= status.HTTP_200_OK)
async def update(
   user_id: UUID,
   update_data: UserUpdate,
   service: UserService = Depends(get_user_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.update(user_id, update_data)


@router.delete("/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete(
   user_id: UUID,
   service: UserService = Depends(get_user_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.delete(user_id)


