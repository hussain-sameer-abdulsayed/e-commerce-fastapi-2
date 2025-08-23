

from typing import List, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, status

from app.db.database import get_db
from app.enums.enums import Discount_Model_Type
from app.services.discount_service import DiscountService
from app.schemas.base_schema import DiscountSetStatus
from app.schemas import CategoryDiscountCreate, CategoryDiscountRead, CategoryDiscountUpdate, ProductDiscountCreate, ProductDiscountRead, ProductDiscountUpdate, ShipmentDiscountCreate, ShipmentDiscountRead, ShipmentDiscountUpdate

list_response_model = Union[
   List[CategoryDiscountRead],
   List[ProductDiscountRead],
   List[ShipmentDiscountRead]
]

single_response_model = Union[
   CategoryDiscountRead,
   ProductDiscountRead,
   ShipmentDiscountRead
]


router = APIRouter(
   responses={404: {"description": "Not found"}}
)


async def get_discount_service(db: AsyncSession = Depends(get_db)) -> DiscountService:
   return DiscountService(db)


@router.get("/{type}", response_model= list_response_model, status_code= status.HTTP_200_OK)
async def get_all_discounts_by_type(
   type: Discount_Model_Type,
   is_active: bool = Query(None, description="Get by active status"),
   service: DiscountService = Depends(get_discount_service)
):
   if is_active is not None:
      return await service.get_by_active_status(type, is_active)
   return await service.get_all(type)


@router.get("/{type}/{discount_id}", response_model= single_response_model, status_code= status.HTTP_200_OK)
async def get_discount_by_id(
   type: Discount_Model_Type,
   discount_id: UUID,
   service: DiscountService = Depends(get_discount_service)
):
   return await service.get_discount_by_id(discount_id, type)


@router.get("/entity/{type}/{entity_id}", response_model= list_response_model, status_code= status.HTTP_200_OK)
async def get_discounts_by_entity_id(
   type: Discount_Model_Type,
   entity_id: UUID,
   is_active: bool = Query(None, description="Get by active status"),
   service: DiscountService = Depends(get_discount_service)
):
   if is_active is not None:
      ### this return only active even if the is_active = false
      return await service.get_active_discounts_by_entity_id(entity_id, type)
   return await service.get_discounts_by_entity_id(entity_id, type)


@router.post("/", response_model= single_response_model, status_code= status.HTTP_201_CREATED)
async def create(
   discount: CategoryDiscountCreate | ProductDiscountCreate | ShipmentDiscountCreate,
   service: DiscountService = Depends(get_discount_service)
):
   return await service.create(discount)


@router.put("/{type}/{discount_id}", response_model= single_response_model, status_code= status.HTTP_200_OK)
async def update(
   type: Discount_Model_Type,
   discount_id: UUID,
   update_data: CategoryDiscountUpdate | ProductDiscountUpdate | ShipmentDiscountUpdate,
   service: DiscountService = Depends(get_discount_service)
):
   return await service.update(discount_id, update_data, type)


@router.delete("/{type}/{discount_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete(
   type: Discount_Model_Type,
   discount_id: UUID,
   service: DiscountService = Depends(get_discount_service)
):
   return await service.delete(discount_id, type)


@router.patch("/set_discount_status/{type}/{discount_id}", status_code= status.HTTP_204_NO_CONTENT)
async def set_discount_status(
   type: Discount_Model_Type,
   discount_id: UUID,
   discount_status: DiscountSetStatus,
   service: DiscountService = Depends(get_discount_service)
):
   return await service.set_discount_status(discount_id, discount_status, type)



