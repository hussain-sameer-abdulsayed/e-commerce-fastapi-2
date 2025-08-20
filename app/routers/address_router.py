from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends, Query, status
from typing import List
from fastapi import APIRouter
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.address import AddressCreate, AddressRead, AddressUpdate
from app.services.address_service import AddressService




router = APIRouter(
   responses={404: {"description":"Not found"}}
)


async def get_address_service(db: AsyncSession = Depends(get_db)) -> AddressService:
   return AddressService(db)


@router.get("/", response_model=List[AddressRead], status_code= status.HTTP_200_OK)
async def get_all_addresses(
   service: AddressService = Depends(get_address_service)
):
   return await service.get_all()


@router.get("/{address_id}", response_model= AddressRead, status_code= status.HTTP_200_OK)
async def get_address_by_id(
   address_id: UUID,
   service: AddressService = Depends(get_address_service)
):
   return await service.get_address(address_id)


@router.get("/seller/{user_id}", response_model= List[AddressRead], status_code= status.HTTP_200_OK)
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






