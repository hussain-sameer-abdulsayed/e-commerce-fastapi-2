
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from app.models.shipment import Shipment
from app.enums.enums import Province



class ShipmentRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_all(self) -> List[Shipment]:
      statement = select(Shipment).order_by(desc(Shipment.created_at))
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[Shipment]:
      statement = select(Shipment).where(Shipment.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_province(self, province: Province) -> Optional[Shipment]:
      statement = select(Shipment).where(Shipment.province == province)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def create(self, shipment: Shipment) -> Shipment:
      self.db.add(shipment)
      await self.db.commit()
      await self.db.refresh(shipment)

      return shipment

   
   async def update(self, shipment: Shipment) -> Shipment:
      self.db.add(shipment)
      await self.db.commit()
      await self.db.refresh(shipment)

      return shipment
   

   async def delete(self, id: UUID) -> bool:
      shipment = await self.get_by_id(id)
      if not shipment:
         return False
      
      await self.db.delete(shipment)
      await self.db.commit()

      return True


   async def exists_by_province(self, province: Province, exclude_id: Optional[UUID] = None) -> bool:
      statement = select(Shipment).where(Shipment.province == province)
      if exclude_id:
         statement = statement.where(Shipment.id != exclude_id)

      result = await self.db.execute(statement)
      shipment = result.first()
      return shipment is not None