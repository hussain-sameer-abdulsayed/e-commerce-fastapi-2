from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from app.models.coupon import Coupon
from app.models.coupon_usage import CouponUsage
from app.schemas import coupon



class CouponRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_all(self) -> List[Coupon]:
      statement = select(Coupon).order_by(desc(Coupon.created_at))
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_code(self, code: UUID) -> Optional[Coupon]:
      statement = (
         select(Coupon)
         .where(Coupon.code == code)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_id(self, id: UUID) -> Optional[Coupon]:
      statement = (
         select(Coupon)
         .where(Coupon.id == id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_active_coupons(self) -> List[Coupon]:
      statement = (
         select(Coupon)
         .where(Coupon.is_currently_active == True)
         .order_by(desc(Coupon.created_at))
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_expire_coupons(self) -> List[Coupon]:
      statement = (
         select(Coupon)
         .where(Coupon.is_currently_active == False)
         .order_by(desc(Coupon.created_at))
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def create(self, coupon: Coupon) -> Coupon:
      self.db.add(coupon)

      await self.db.commit()
      await self.db.refresh(coupon)

      return coupon


   async def update(self, coupon: Coupon) -> Coupon:
      coupon.updated_at = datetime.utcnow()
      self.db.add(coupon)
      await self.db.commit()

      await self.db.refresh(coupon)

      return coupon


   async def delete(self, id: UUID) -> bool:
      coupon = await self.get_by_id(id)
      if coupon:
         await self.db.delete(coupon)
         await self.db.commit()

         return True
      return False


   async def set_coupon_active_status(self, id: UUID, is_active: bool) -> bool:
      pass

   ### or move it to cart repository
   async def apply_coupon_to_cart(self, code: UUID, cart_id: UUID) -> bool:
      pass


   async def get_coupon_usages(self) -> List[CouponUsage]:
      statement = select(CouponUsage).order_by(desc(CouponUsage.used_at))
      result = await self.db.execute(statement)
      return list(result.scalars().all())

   
   async def get_coupon_usages_by_coupon_id(self, coupon_id: UUID) -> List[CouponUsage]:
      statement = (
         select(CouponUsage)
         .where(CouponUsage.coupon_id == coupon_id)
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())



   async def get_coupon_usage_by_id(self, id: UUID) -> Optional[CouponUsage]:
      statement = (
         select(CouponUsage)
         .where(CouponUsage.id == id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_coupon_usage_by_user_id(self, user_id: UUID) -> Optional[CouponUsage]:
      statement = (
         select(CouponUsage)
         .where(CouponUsage.user_id == user_id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   


