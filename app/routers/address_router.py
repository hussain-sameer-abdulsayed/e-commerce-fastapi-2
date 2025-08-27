from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends, Query, status
from typing import List
from fastapi import APIRouter
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.address import AddressCreate, AddressRead, AddressUpdate
from app.services.address_service import AddressService
from app.authentication.auth_dependency import (
   require_user,
   require_admin,
   require_seller,
   get_current_verified_user,
   get_current_active_user
)




router = APIRouter(
   responses={404: {"description":"Not found"}}
)


async def get_address_service(db: AsyncSession = Depends(get_db)) -> AddressService:
   return AddressService(db)


@router.get("/", response_model=List[AddressRead], status_code= status.HTTP_200_OK)
async def get_all_addresses(
   service: AddressService = Depends(get_address_service),
   current_user: User = Depends(require_admin)
):
   return await service.get_all()


@router.get("/{address_id}", response_model= AddressRead, status_code= status.HTTP_200_OK)
async def get_address_by_id(
   address_id: UUID,
   service: AddressService = Depends(get_address_service)
):
   return await service.get_address(address_id)


@router.get("/user/{user_id}", response_model= List[AddressRead], status_code= status.HTTP_200_OK)
async def get_addresses_by_user_id(
   user_id: UUID,
   service: AddressService = Depends(get_address_service)
):
   return await service.get_addresses_by_user_id(user_id)


@router.get("/seller/{seller_id}", response_model= List[AddressRead], status_code= status.HTTP_200_OK)
async def get_addresses_by_seller_id(
   seller_id: UUID,
   service: AddressService = Depends(get_address_service)
):
   return await service.get_addresses_by_seller_id(seller_id)


@router.post("/", response_model= AddressRead, status_code= status.HTTP_201_CREATED)
async def create_address(
   address: AddressCreate,
   service: AddressService = Depends(get_address_service),
   current_user: User = Depends(get_current_verified_user)
):
   ### should get user_id or seller_id from token sent
   return await service.create(current_user.id, address)


@router.put("/{address_id}", response_model= AddressRead, status_code= status.HTTP_200_OK)
async def update_address(
   address_id: UUID,
   update_address: AddressUpdate,
   service: AddressService = Depends(get_address_service),
   current_user: User = Depends(get_current_verified_user)
):
   return await service.update(address_id, update_address)


@router.delete("/{address_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_address(
   address_id: UUID,
   service: AddressService = Depends(get_address_service),
   current_user: User = Depends(get_current_verified_user)
):
   return await service.delete(address_id)



