from __future__ import annotations
from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import SQLModel
from app.repositories.base_repository import BaseRepository


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
   def __init__(self, repository: BaseRepository[ModelType]):
      self.repository = repository


   async def create(self, obj_in: CreateSchemaType) -> ModelType:
      obj_data = obj_in.model_dump()
      db_obj = self.repository.model(**obj_data)
      return await self.repository.create(db_obj)
   

   async def get_by_id(self, id: UUID) -> Optional[ModelType]:
      return await self.repository.get_by_id(id)


   async def get_all(self) -> List[ModelType]:
      return await self.repository.get_all()
   

   async def update(self, id: UUID, obj_in: UpdateSchemaType) -> Optional[ModelType]:
      db_obj = await self.repository.get_by_id(id)
      if not db_obj:
         return None
      
      obj_data = jsonable_encoder(obj_in)
      for field, value in obj_data.items():
         if hasattr(db_obj, field):
            setattr(db_obj, field, value)

      return await self.repository.update(db_obj)
   

   async def delete(self, id: UUID) -> bool:
      return await self.repository.delete(id)