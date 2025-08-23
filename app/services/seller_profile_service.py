from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.seller_profile import SellerProfile
from app.models.user import User
from app.repositories.seller_profile_repository import SellerProfileRepository
from app.schemas.seller_profile import SellerProfileCreate, SellerProfileRead, SellerProfileUpdate


class SellerProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = SellerProfileRepository(db)
    
    async def get_all_sellers(self) -> List[SellerProfileRead]:
        sellers = await self.repository.get_all()
        return [SellerProfileRead.model_validate(seller) for seller in sellers]
    

    async def get_all_active_sellers(self, is_active: bool) -> List[SellerProfileRead]:
        sellers = await self.repository.get_all_active(is_active)
        return [SellerProfileRead.model_validate(seller) for seller in sellers]
    

    async def get_all_verified_sellers(self, is_verified: bool) -> List[SellerProfileRead]:
        sellers = await self.repository.get_all_verified(is_verified)
        return [SellerProfileRead.model_validate(seller) for seller in sellers]
    

    async def get_seller_by_id(self, seller_id: UUID) -> SellerProfileRead:
        seller = await self.repository.get_by_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def get_seller_by_user_id(self, user_id: UUID) -> SellerProfileRead:
        seller = await self.repository.get_by_user_id(user_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def get_seller_by_store_name(self, store_name: str) -> SellerProfileRead:
        seller = await self.repository.get_by_store_name(store_name)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def get_seller_with_user(self, seller_id: UUID) -> SellerProfile:
        seller = await self.repository.get_with_user(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return seller
    
    
    async def create_seller_profile(self, seller_data: SellerProfileCreate, exclude_id: UUID) -> SellerProfileRead:
        # Check if user exists
        user = await self.db.get(User, seller_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )
        
        # Check if store name already exists
        if await self.repository.exists_by_store_name(seller_data.store_name, exclude_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Store with name '{seller_data.store_name}' already exists"
            )
        
        # Check if phone number already exists
        phone_str = str(seller_data.store_phone_number)
        if await self.repository.exists_by_store_phone(phone_str, exclude_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Store with phone number '{phone_str}' already exists"
            )
        
        # Create seller profile
        seller_dict = seller_data.model_dump()
        seller_dict["store_phone_number"] = phone_str  # Convert phone to string
        seller = SellerProfile(**seller_dict)
        
        # Save to database
        created_seller = await self.repository.create(seller)
        
        return SellerProfileRead.model_validate(created_seller)
    

    async def update_seller_profile(self, seller_id: UUID, update_data: SellerProfileUpdate) -> SellerProfileRead:
        seller = await self.repository.get_by_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Check if store name is being updated and if it already exists
        if "store_name" in update_dict and update_dict["store_name"] != seller.store_name:
            exists = await self.repository.exists_by_store_name(update_dict["store_name"], exclude_id=seller_id)
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Store with name '{update_dict['store_name']}' already exists"
                )
        
        # Check if phone number is being updated and if it already exists
        if "store_phone_number" in update_dict and update_dict["store_phone_number"]:
            phone_str = str(update_dict["store_phone_number"])
            if phone_str != seller.store_phone_number:
                exists = await self.repository.exists_by_store_phone(phone_str, exclude_id=seller_id)
                if exists:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Store with phone number '{phone_str}' already exists"
                    )
                update_dict["store_phone_number"] = phone_str
        
        # Update fields
        for field, value in update_dict.items():
            if hasattr(seller, field) and value is not None:
                setattr(seller, field, value)
        
        # Save updates
        updated_seller = await self.repository.update(seller)
        
        return SellerProfileRead.model_validate(updated_seller)
    

    async def update_seller_by_user_id(self, user_id: UUID, update_data: SellerProfileUpdate) -> SellerProfileRead:
        seller = await self.repository.get_by_user_id(user_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        
        return await self.update_seller_profile(seller.id, update_data)
    

    async def verify_seller(self, seller_id: UUID) -> SellerProfileRead:
        seller = await self.repository.verify_seller(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def activate_seller(self, seller_id: UUID) -> SellerProfileRead:
        seller = await self.repository.activate_seller(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def deactivate_seller(self, seller_id: UUID) -> SellerProfileRead:
        seller = await self.repository.deactivate_seller(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return SellerProfileRead.model_validate(seller)
    

    async def delete_seller_profile(self, seller_id: UUID) -> bool:
        result = await self.repository.delete(seller_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        return result
    

    async def delete_seller_by_user_id(self, user_id: UUID) -> bool:
        seller = await self.repository.get_by_user_id(user_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller profile not found"
            )
        
        return await self.repository.delete(seller.id)
    

