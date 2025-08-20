
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.enums.enums import Province
from app.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.db.database import get_db
from app.services.shipment_service import ShipmentService


router = APIRouter(
   responses={404:{"Description":"Not found"}}
)


async def get_shipment_service(db: AsyncSession = Depends(get_db)) -> ShipmentService:
   return ShipmentService(db)


@router.get("/", response_model= List[ShipmentRead], status_code= status.HTTP_200_OK)
async def get_all(
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.get_all()


@router.get("/{shipment_id}", response_model= ShipmentRead, status_code= status.HTTP_200_OK)
async def get_by_id(
   shipment_id: UUID,
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.get_by_id(shipment_id)


@router.get("/province/{province}", response_model= ShipmentRead, status_code= status.HTTP_200_OK)
async def get_by_province(
   province: Province,
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.get_by_province(province)


@router.post("/", response_model= ShipmentRead, status_code= status.HTTP_201_CREATED)
async def create_shipment(
   shipment: ShipmentCreate,
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.create(shipment)


@router.put("/{shipment_id}", response_model= ShipmentRead, status_code= status.HTTP_200_OK)
async def update_shipment(
   shipment_id: UUID,
   update_data: ShipmentUpdate,
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.update(shipment_id, update_data)


@router.delete("/{shipment_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_shipment(
   shipment_id: UUID,
   service: ShipmentService = Depends(get_shipment_service)
):
   return await service.delete(shipment_id)

   