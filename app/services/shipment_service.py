from __future__ import annotations
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.enums.enums import Province
from app.models.shipment import Shipment
from app.repositories.shipment_repository import ShipmentRepository
from app.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate


class ShipmentService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = ShipmentRepository(db)


   async def get_all(self) -> List[ShipmentRead]:
      shipments = await self.repository.get_all()
      return [ShipmentRead.model_validate(shipment) for shipment in shipments]
   

   async def get_by_id(self, id: UUID) -> Optional[ShipmentRead]:
      shipment = await self.repository.get_by_id(id)
      if not shipment:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Shipment not found"
         )
      return ShipmentRead.model_validate(shipment)


   async def get_by_province(self, province: Province) -> Optional[ShipmentRead]:
      shipment = await self.repository.get_by_province(province)
      if not shipment:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Shipment not found"
         )
      return ShipmentRead.model_validate(shipment)

   async def create(self, shipment_data: ShipmentCreate) -> ShipmentRead:
      shipment = Shipment(**shipment_data.model_dump())

      if await self.repository.exists_by_province(shipment.province):
         raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= f"Shipment with province {shipment.province} is already exists"
            )

      created_shipment = await self.repository.create(shipment)
      return ShipmentRead.model_validate(created_shipment)
   

   async def update(self, id: UUID, update_data: ShipmentUpdate) -> ShipmentRead:
      shipment = await self.repository.get_by_id(id)
      if not shipment:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Shipment not found"
         )
      
      update_dict = update_data.model_dump(exclude_unset= True)

      if "province" in update_dict and update_dict["province"] != shipment.province:
         if await self.repository.exists_by_province(update_dict["province"]):
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= f"Shipment with province {update_dict['province']} is already exists"
            )
         
      for field, value in update_dict.items():
         if hasattr(shipment, field) and value is not None:
            setattr(shipment, field, value)

      updated_shipment = await self.repository.update(shipment)

      return ShipmentRead.model_validate(updated_shipment)


   async def delete(self, id:UUID) -> bool:
      result = await self.repository.delete(id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Shipment not found"
         )
      return result

   