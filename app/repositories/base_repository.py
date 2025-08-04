from __future__ import annotations
from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlmodel import SQLModel, select, func
from sqlalchemy.ext.asyncio import AsyncSession



ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
   def __init__(self, model: Type[ModelType], db: AsyncSession):
      self.model = model
      self.db = db


   ### Create a new object ###
   async def create(self, obj: ModelType) -> ModelType:
      self.db.add(obj)
      await self.db.commit()
      await self.db.refresh(obj)
      return obj
   

   async def get_by_id(self, id: UUID) -> Optional[ModelType]:
      return await self.db.get(self.model, id)
   

   async def get_all(self) -> List[ModelType]:
      statement = select(self.model)
      result = await self.db.execute(statement)
      return result.scalars().all()
   

   async def update(self, obj: ModelType) -> ModelType:
      self.db.add(obj)
      await self.db.commit()
      await self.db.refresh(obj)
      return obj
   

   async def delete(self, id: UUID) -> bool:
      obj = await self.get_by_id(id)
      if obj:
         await self.db.delete(obj)
         await self.db.commit()
         return True
      return False