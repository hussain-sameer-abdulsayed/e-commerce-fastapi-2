 
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.database import get_db
from app.models.user import User
from app.services.user_profile_service import UserProfileService
from app.schemas.user_profile import UserProfileCreate, UserProfileRead, UserProfileUpdate
from app.authentication.auth_dependency import (
   require_admin,
   require_user,
   get_current_active_user
)



router = APIRouter(
   responses={404: {"description": "Not found"}}
)


async def get_user_profile_service(db: AsyncSession = Depends(get_db)) -> UserProfileService:
   return UserProfileService(db)


@router.get("/", response_model= List[UserProfileRead], status_code= status.HTTP_200_OK)
async def get_all(
   service: UserProfileService = Depends(get_user_profile_service)
):
   return await service.get_all()


@router.get("/with-user/{profile_id}", response_model= UserProfileRead, status_code= status.HTTP_200_OK)
async def get_with_profiles(
   profile_id: UUID,
   service: UserProfileService = Depends(get_user_profile_service)
):
   return await service.get_with_user(profile_id)


@router.get("/user/{user_id}", response_model= UserProfileRead, status_code= status.HTTP_200_OK)
async def get_by_user_id(
   user_id: UUID,
   service: UserProfileService = Depends(get_user_profile_service)
):
   return await service.get_by_user_id(user_id)


@router.get("/{profile_id}", response_model= UserProfileRead, status_code= status.HTTP_200_OK)
async def get_by_id(
   profile_id: UUID,
   service: UserProfileService = Depends(get_user_profile_service)
):
   return await service.get_by_id(profile_id)


@router.post("/", response_model= UserProfileRead, status_code= status.HTTP_201_CREATED)
async def create(
   profile_data: UserProfileCreate,
   service: UserProfileService = Depends(get_user_profile_service),
   current_user: User = Depends(require_user)
):
   return await service.create(profile_data)


@router.put("/user/{user_id}", response_model= UserProfileRead, status_code= status.HTTP_200_OK)
async def update_by_user_id(
   user_id: UUID,
   update_data: UserProfileUpdate,
   service: UserProfileService = Depends(get_user_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.update_profile_by_user_id(user_id, update_data)


@router.put("/{profile_id}", response_model= UserProfileRead, status_code= status.HTTP_200_OK)
async def update(
   profile_id: UUID,
   update_data: UserProfileUpdate,
   service: UserProfileService = Depends(get_user_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   return await service.update(profile_id, update_data)


@router.delete("/user/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_by_user_id(
   user_id: UUID,
   service: UserProfileService = Depends(get_user_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.delete_profile_by_user_id(user_id)


@router.delete("/{profile_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete(
   profile_id: UUID,
   service: UserProfileService = Depends(get_user_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   return await service.delete(profile_id)


