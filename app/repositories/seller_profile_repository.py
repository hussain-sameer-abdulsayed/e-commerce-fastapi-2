from datetime import datetime
from typing import List, Optional
from unittest import result
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select
from sqlalchemy.orm import selectinload

from app.models.seller_profile import SellerProfile





class SellerProfileRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_all(self) -> List[SellerProfile]:
      statement = select(SellerProfile)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[SellerProfile]:
      statement = select(SellerProfile).where(SellerProfile.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_user_id(self, user_id: UUID) -> Optional[SellerProfile]:
      statement = select(SellerProfile).where(SellerProfile.user_id == user_id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_with_user(self, id: UUID) -> Optional[SellerProfile]:
      statement = (
         select(SellerProfile)
         .options(
            selectinload(SellerProfile.user)
         )
         .where(SellerProfile.id == id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_store_name(self, store_name: str) -> Optional[SellerProfile]:
      statement = select(SellerProfile).where(SellerProfile.store_name == store_name)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()

   async def get_by_phone(self, phone: str) -> Optional[SellerProfile]:
      statement = select(SellerProfile).where(SellerProfile.store_phone_number == phone)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_all_active(self, is_active: bool) -> List[SellerProfile]:
      statement = (
         select(SellerProfile)
         .where(SellerProfile.is_active == is_active)
         .order_by(desc(SellerProfile.created_at))
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_all_verified(self, is_verified: bool) -> List[SellerProfile]:
      statement = (
         select(SellerProfile)
         .where(SellerProfile.is_verified == is_verified)
         .order_by(desc(SellerProfile.created_at))
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def create(self, profile: SellerProfile) -> SellerProfile:
      self.db.add(profile)
      await self.db.commit()
      await self.db.refresh(profile)
      return profile


   async def update(self, profile: SellerProfile) -> SellerProfile:
      profile.updated_at = datetime.utcnow()
      self.db.add(profile)
      await self.db.commit()
      await self.db.refresh(profile)
      return profile


   async def delete(self, id: UUID) -> bool:
      profile = await self.get_by_id(id)
      if not profile:
         return False
      await self.db.delete(profile)
      await self.db.commit()
      return True
   

   async def exists_by_store_name(self, store_name: str, exclude_id: UUID) -> bool:
      statement = select(SellerProfile).where(SellerProfile.store_name == store_name)
      if exclude_id:
         statement = statement.where(SellerProfile.id != exclude_id)

      result = await self.db.execute(statement)
      profile = result.scalar_one_or_none()
      return profile is not None

   
   async def exists_by_store_phone(self, phone: str, exclude_id: UUID) -> bool:
      statement = select(SellerProfile).where(SellerProfile.store_phone_number == phone)
      if exclude_id:
         statement = statement.where(SellerProfile.id != exclude_id)

      result = await self.db.execute(statement)
      profile = result.scalar_one_or_none()
      return profile is not None


   async def verify_seller(self, seller_id: UUID) -> Optional[SellerProfile]:
      profile = await self.get_by_id(seller_id)
      if not profile:
         return None
      
      profile.is_verified = True
      return await self.update(profile)


   async def activate_seller(self, seller_id: UUID) -> Optional[SellerProfile]:
      profile = await self.get_by_id(seller_id)
      if not profile:
         return None
      
      profile.is_active = True
      return await self.update(profile)
   

   async def deactivate_seller(self, seller_id: UUID) -> Optional[SellerProfile]:
      profile = await self.get_by_id(seller_id)
      if not profile:
         return None
      
      profile.is_active = False
      return await self.update(profile)



### add get_with_products , search  and full text searchfor store name and description
