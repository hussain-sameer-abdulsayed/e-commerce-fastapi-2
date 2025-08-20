from __future__ import annotations
from typing import List
from fastapi import HTTPException, APIRouter, Depends, Query, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.cart_router import get_cart_service
from app.services.coupon_service import CouponService
from app.db.database import get_db
from app.schemas.coupon import CouponCreate, CouponRead, CouponUpdate, CouponSetStatus
from app.schemas.coupon_usage import CouponUsageCreate, CouponUsageRead


router = APIRouter(
   responses={404: {"description":"Not found"}}
)


async def get_coupon_service(db: AsyncSession = Depends(get_db)) -> CouponService:
   return CouponService(db)




@router.get("/", response_model= List[CouponRead], status_code= status.HTTP_200_OK)
async def get_coupons(
   is_active: bool = Query(None, description="return active or expire coupons"),
   service: CouponService = Depends(get_coupon_service)
):
   if is_active is not None:
      return await service.get_coupons_by_active_status(is_active)
   
   return await service.get_all_coupons()


@router.get("/coupon-usages", response_model= List[CouponUsageRead], status_code= status.HTTP_200_OK)
async def get_all_coupon_usages(
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_all_coupon_usages()


@router.get("/code/{code}", response_model= CouponRead, status_code= status.HTTP_200_OK)
async def get_coupon_by_code(
   code: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_by_code(code)


@router.get("/{coupon_id}", response_model= CouponRead, status_code= status.HTTP_200_OK)
async def get_coupon_by_id(
   coupon_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_by_id(coupon_id)


@router.get("/coupon-usages/{coupon_usage_id}", response_model= CouponUsageRead, status_code= status.HTTP_200_OK)
async def get_coupon_usage_by_id(
   coupon_usage_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_coupon_usage_by_id(coupon_usage_id)


@router.get("/coupon-usages/coupon/{coupon_id}", response_model= List[CouponUsageRead], status_code= status.HTTP_200_OK)
async def get_coupon_usages_by_coupon_id(
   coupon_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_coupon_usages_by_coupon_id(coupon_id)


@router.get("/coupon-usages/user/{user_id}", response_model= List[CouponUsageRead], status_code= status.HTTP_200_OK)
async def get_coupon_usages_by_user_id(
   user_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.get_coupon_usages_by_user_id(user_id)



@router.patch("/{coupon_id}", response_model= bool, status_code= status.HTTP_200_OK)
async def set_coupon_active_status(
   coupon_set_status: CouponSetStatus,
   coupon_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.set_coupon_active_status(coupon_id, coupon_set_status)


@router.post("/", response_model= CouponRead, status_code= status.HTTP_201_CREATED)
async def create_coupon(
   coupon: CouponCreate,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.create_coupon(coupon)


@router.put("/{coupon_id}", response_model= CouponRead, status_code= status.HTTP_200_OK)
async def update_coupon(
   coupon_id: UUID,
   coupon_update: CouponUpdate,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.update_coupon(coupon_id, coupon_update)


@router.delete("/{coupon_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_coupon(
   coupon_id: UUID,
   service: CouponService = Depends(get_coupon_service)
):
   return await service.delete_coupon(coupon_id)




