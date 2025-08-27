from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_profile import UserProfile
from app.models.user import User
from app.repositories.user_profile_repository import UserProfileRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_profile import UserProfileCreate, UserProfileRead, UserProfileUpdate


class UserProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserProfileRepository(db)
        self.user_repository = UserRepository(db)
    


    async def get_all(self) -> List[UserProfileRead]:
        profiles = await self.repository.get_all()
        return [UserProfileRead.model_validate(profile) for profile in profiles]
    

    async def get_by_id(self, profile_id: UUID) -> UserProfileRead:
        profile = await self.repository.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return UserProfileRead.model_validate(profile)
    

    async def get_by_user_id(self, user_id: UUID) -> UserProfileRead:
        profile = await self.repository.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return UserProfileRead.model_validate(profile)
    

    async def get_with_user(self, profile_id: UUID) -> UserProfile:
        profile = await self.repository.get_with_user(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return profile
    
    
    async def create(self, profile_data: UserProfileCreate) -> UserProfileRead:
        # Check if user exists
        user = await self.user_repository.get_by_id(profile_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )
        
        # Check if user has a profile 
        exists = await self.repository.get_by_user_id(profile_data.user_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"User with username {user.user_name} has a profile"
            )
        
        # Create profile
        profile = UserProfile(**profile_data.model_dump())
        
        # Save to database
        created_profile = await self.repository.create(profile)
        
        return UserProfileRead.model_validate(created_profile)
    

    async def update(self, profile_id: UUID, update_data: UserProfileUpdate) -> UserProfileRead:
        profile = await self.repository.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Update fields
        for field, value in update_dict.items():
            if hasattr(profile, field) and value is not None:
                setattr(profile, field, value)
        
        # Save updates
        updated_profile = await self.repository.update(profile)
        
        return UserProfileRead.model_validate(updated_profile)
    

    async def update_profile_by_user_id(self, user_id: UUID, update_data: UserProfileUpdate) -> UserProfileRead:
        profile = await self.repository.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Update fields
        for field, value in update_dict.items():
            if hasattr(profile, field) and value is not None:
                setattr(profile, field, value)
        
        # Save updates
        updated_profile = await self.repository.update(profile)
        
        return UserProfileRead.model_validate(updated_profile)
    

    async def delete(self, profile_id: UUID) -> bool:
        result = await self.repository.delete(profile_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return result
    

    async def delete_profile_by_user_id(self, user_id: UUID) -> bool:
        profile = await self.repository.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        return await self.repository.delete(profile.id)
    

