from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select
from uuid import UUID
from app.enums.enums import Order_Status
from app.models.order import Order


class OrderRepository:
   def __init__(self, db: AsyncSession):
      self.db = db

   
   async def get_all(self) -> List[Order]:
      statement = select(Order).order_by(desc(Order.created_at))
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[Order]:
      statement = select(Order).where(Order.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_by_order_number(self, order_number: UUID) -> Optional[Order]:
      statement = select(Order).where(Order.order_number == order_number)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_status(self, status: Order_Status) -> List[Order]:
      statement = select(Order).order_by(desc(Order.status == status))
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def create(self, order: Order) -> Order:
      self.db.add(order)
      await self.db.commit()
      await self.db.refresh(order)
      return order
   

   async def update(self, order: Order) -> Order:
      order.updated_at = datetime.utcnow()
      self.db.add(order)
      await self.db.commit()
      await self.db.refresh(order)
      return order


   async def delete(self, id: UUID) -> bool:
      order = await self.get_by_id(id)
      if not order:
         return False
      await self.db.delete(order)
      await self.db.commit()
      return True
   

   async def update_status(self, id: UUID, status: Order_Status) -> Optional[Order]:
      order = await self.get_by_id(id)
      if not order:
         return None
      
      order.status = status
      order.updated_at = datetime.utcnow()
      await self.db.commit()
      await self.db.refresh(order)
      return order


