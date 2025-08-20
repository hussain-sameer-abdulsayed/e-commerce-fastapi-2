
from tkinter.tix import STATUS
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coupon import Coupon
from app.repositories.coupon_repository import CouponRepository
from app.schemas.coupon import CouponRead, CouponCreate, CouponSetStatus, CouponUpdate
from app.schemas.coupon_usage import CouponUsageRead


class CouponService:
   def __init__(self, db: AsyncSession) -> None:
      self.db = db
      self.repository = CouponRepository(db)
      

   
   async def get_all_coupons(self) -> List[CouponRead]:
      coupons = await self.repository.get_all()
      return [CouponRead.model_validate(coupon) for coupon in coupons]


   async def get_by_code(self, code: UUID) -> Optional[CouponRead]:
      coupon = await self.repository.get_by_code(code)
      if not coupon:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
         )
      return CouponRead.model_validate(coupon)


   async def get_by_id(self, id: UUID) -> Optional[CouponRead]:
      coupon = await self.repository.get_by_id(id)
      if not coupon:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
         )
      return CouponRead.model_validate(coupon)


   async def get_coupons_by_active_status(self, is_active: bool) -> List[CouponRead]:
      coupons = await self.repository.get_coupons_by_active_status(is_active)
      return [CouponRead.model_validate(coupon) for coupon in coupons]


   async def get_all_coupon_usages(self) -> List[CouponUsageRead]:
      usages = await self.repository.get_coupon_usages ()
      return [CouponUsageRead.model_validate(usage) for usage in usages]


   async def get_coupon_usages_by_coupon_id(self, id: UUID) -> List[CouponUsageRead]:
      usages = await self.repository.get_coupon_usages_by_coupon_id(id)
      return [CouponUsageRead.model_validate(usage) for usage in usages]
   

   async def get_coupon_usages_by_user_id(self, id: UUID) -> List[CouponUsageRead]:
      usages = await self.repository.get_coupon_usages_by_user_id(id)
      return [CouponUsageRead.model_validate(usage) for usage in usages]


   async def get_coupon_usage_by_id(self, id: UUID) -> Optional[CouponUsageRead]:
      coupon_usage = await self.repository.get_coupon_usage_by_id(id)
      if not coupon_usage:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Coupon usage not found"
         )
      return CouponUsageRead.model_validate(coupon_usage)


   async def set_coupon_active_status(self, coupon_id: UUID, coupon_set_status: CouponSetStatus) -> bool:
      success = await self.repository.set_coupon_active_status(coupon_id, coupon_set_status)

      if not success:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Coupon does not exsits or you entered the same status"
         )
      
      return success
   

   async def create_coupon(self, coupon_create: CouponCreate) -> CouponRead:
      coupon = Coupon(**coupon_create.model_dump())

      created_coupon = await self.repository.create(coupon)

      return CouponRead.model_validate(created_coupon)


   async def update_coupon(self, id: UUID, coupon_update: CouponUpdate) -> CouponRead:
      coupon = await self.repository.get_by_id(id)
      if not coupon:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Coupon not found"
         )
      
      coupon_dict = coupon_update.model_dump(exclude_unset= True)

      for field, value in coupon_dict.items():
         if hasattr(coupon, field) and value is not None:
            setattr(coupon, field, value)

      updated_coupon = await self.repository.update(coupon)

      return CouponRead.model_validate(updated_coupon)


   async def delete_coupon(self, id: UUID) -> bool:
      result = await self.repository.delete(id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Coupon not found"
         )
      return result









