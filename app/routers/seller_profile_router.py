 
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query, status

from pydantic_extra_types.phone_numbers import PhoneNumber

from app.models.user import User
PhoneNumber.phone_format = 'E164'
from app.db.database import get_db
from app.services.seller_profile_service import SellerProfileService
from app.schemas.seller_profile import SellerProfileCreate, SellerProfileRead, SellerProfileUpdate
from app.authentication.auth_dependency import (
   require_seller,
   require_admin,
   get_current_active_user
)



router = APIRouter(
   responses={404: {"description": "Not found"}}
)


async def get_seller_profile_service(db: AsyncSession = Depends(get_db)) -> SellerProfileService:
   return SellerProfileService(db)


@router.get("/", response_model= List[SellerProfileRead], status_code= status.HTTP_200_OK)
async def get_all(
   is_active: bool = Query(None, description="For return profiles by active status"),
   is_verified: bool = Query(None, description="For return profiles by verify status"),
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(require_admin)
):
   if is_active is not None:
      return await service.get_all_active(is_active)
   elif is_verified is not None:
      return await service.get_all_verified(is_verified)
   
   return await service.get_all()


@router.get("/with-user/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def get_with_profiles(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service)
):
   return await service.get_with_user(seller_id)


@router.get("/user/{user_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def get_by_user_id(
   user_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service)
):
   return await service.get_by_user_id(user_id)


@router.get("/store/{store_name}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def get_by_store_name(
   store_name: str,
   service: SellerProfileService = Depends(get_seller_profile_service)
):
   return await service.get_by_store_name(store_name)


@router.get("/phone/{phone}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def get_by_phone(
   phone: PhoneNumber,
   service: SellerProfileService = Depends(get_seller_profile_service)
):
   return await service.get_by_phone(str(phone))


@router.get("/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def get_by_id(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service)
):
   return await service.get_by_id(seller_id)


@router.post("/", response_model= SellerProfileRead, status_code= status.HTTP_201_CREATED)
async def create(
   profile_data: SellerProfileCreate,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(require_seller)
):
   return await service.create(profile_data)


@router.put("/user/{user_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def update_by_user_id(
   user_id: UUID,
   update_data: SellerProfileUpdate,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.update_profile_by_user_id(user_id, update_data)


@router.put("/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def update(
   seller_id: UUID,
   update_data: SellerProfileUpdate,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   return await service.update(seller_id, update_data)


@router.delete("/user/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_by_user_id(
   user_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   if current_user.id != user_id and current_user.role != "admin":
      raise HTTPException(403, "Not Authorized")
   return await service.delete_profile_by_user_id(user_id)


@router.delete("/{seller_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(get_current_active_user)
):
   return await service.delete(seller_id)


@router.patch("/verify-seller/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def verify_seller(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(require_admin)
):
   return await service.verify_seller(seller_id)


@router.patch("/activate-seller/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def activate_seller(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(require_admin)
):
   return await service.activate_seller(seller_id)


@router.patch("/deactivate-seller/{seller_id}", response_model= SellerProfileRead, status_code= status.HTTP_200_OK)
async def deactivate_seller(
   seller_id: UUID,
   service: SellerProfileService = Depends(get_seller_profile_service),
   current_user: User = Depends(require_admin)
):
   return await service.deactivate_seller(seller_id)


