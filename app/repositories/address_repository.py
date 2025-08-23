
from datetime import datetime
from re import A
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from app.models.address import Address



class AddressRepository:
   def __init__(self, db: AsyncSession) -> None:
      self.db = db


   async def get_all(self) -> List[Address]:
      statement = select(Address).order_by(desc(Address.created_at))
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_address(self, id: UUID) -> Optional[Address]:
      statement = select(Address).where(Address.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_addresses_by_user_id(self, user_id: UUID) -> List[Address]:
      statement = select(Address).where(Address.user_id == user_id)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_addresses_by_seller_id(self, seller_id: UUID) -> List[Address]:
      statement = select(Address).where(Address.seller_profile_id == seller_id)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def create(self, address: Address) -> Address:
      self.db.add(address)
      await self.db.commit()
      await self.db.refresh(address)

      return address


   async def update(self, address: Address) -> Address:
      address.updated_at = datetime.utcnow()
      self.db.add(address)
      await self.db.commit()
      await self.db.refresh(address)

      return address


   async def delete(self, id: UUID) -> bool:
      address = await self.get_address(id)
      if not address:
         return False
      
      await self.db.delete(address)
      await self.db.commit()

      return True


