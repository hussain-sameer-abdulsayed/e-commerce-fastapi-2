from __future__ import annotations
from typing import List, Optional, Union
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.enums import Discount_Model_Type
from app.models import CategoryDiscount, ProductDiscount
from app.models.shipment_discount import ShipmentDiscount
from app.repositories import CategoryRepository, ProductRepository, ShipmentRepository, DiscountRepository

from app.schemas.base_schema import DiscountSetStatus
from app.schemas import (
    CategoryDiscountCreate, CategoryDiscountRead, CategoryDiscountUpdate,
    ProductDiscountCreate, ProductDiscountRead, ProductDiscountUpdate,
    ShipmentDiscountCreate, ShipmentDiscountRead, ShipmentDiscountUpdate
)

# Type aliases for cleaner annotations
DiscountRead = Union[CategoryDiscountRead, ProductDiscountRead, ShipmentDiscountRead]
DiscountReadList = List[DiscountRead]
DiscountCreate = Union[CategoryDiscountCreate, ProductDiscountCreate, ShipmentDiscountCreate]
DiscountUpdate = Union[CategoryDiscountUpdate, ProductDiscountUpdate, ShipmentDiscountUpdate]

# Mapping from type to schema
MODEL_MAP = {
    Discount_Model_Type.CATEGORY: CategoryDiscountRead,
    Discount_Model_Type.PRODUCT: ProductDiscountRead,
    Discount_Model_Type.SHIPMENT: ShipmentDiscountRead
}

class DiscountService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = DiscountRepository(db)
        self.category_repository = CategoryRepository(db)
        self.product_repository = ProductRepository(db)
        self.shipment_repository = ShipmentRepository(db)

    # ---------------- List endpoints ----------------
    async def get_all(self, type: Discount_Model_Type) -> DiscountReadList:
        discounts = await self.repository.get_all(type)
        return [MODEL_MAP[type].model_validate(dis) for dis in discounts]


    async def get_by_active_status(self, type: Discount_Model_Type, is_active: bool) -> DiscountReadList:
        discounts = await self.repository.get_by_active_status(type, is_active)
        return [MODEL_MAP[type].model_validate(dis) for dis in discounts]


    async def get_discounts_by_entity_id(self, id: UUID, type: Discount_Model_Type) -> DiscountReadList:
        discounts = await self.repository.get_discounts_by_entity_id(id, type)
        return [MODEL_MAP[type].model_validate(dis) for dis in discounts]


    async def get_active_discounts_by_entity_id(self, id: UUID, type: Discount_Model_Type) -> DiscountReadList:
        discounts = await self.repository.get_active_discounts_by_entity_id(id, type)
        return [MODEL_MAP[type].model_validate(dis) for dis in discounts]


    # ---------------- Single-resource endpoint ----------------
    async def get_discount_by_id(self, id: UUID, type: Discount_Model_Type) -> Optional[DiscountRead]:
        discount = await self.repository.get_discount_by_id(id, type)
        if discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return MODEL_MAP[type].model_validate(discount)


    # ---------------- Create ----------------
    async def create(self, discount_data: DiscountCreate) -> DiscountRead:
        # Validate entity exists
        repo_map = {
            Discount_Model_Type.CATEGORY: self.category_repository,
            Discount_Model_Type.PRODUCT: self.product_repository,
            Discount_Model_Type.SHIPMENT: self.shipment_repository
        }

        repository = repo_map[discount_data.discount_type]
        exists = await repository.get_by_id(discount_data.entity_id)
        if not exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{discount_data.discount_type.name} not found")

        # Create discount object
        discount_obj_map = {
            Discount_Model_Type.CATEGORY: CategoryDiscount(category_id=discount_data.entity_id,), # type: ignore
            Discount_Model_Type.PRODUCT: ProductDiscount(product_id=discount_data.entity_id), # type: ignore
            Discount_Model_Type.SHIPMENT: ShipmentDiscount(shipment_id=discount_data.entity_id) # type: ignore
        }

        discount = discount_obj_map[discount_data.discount_type]
        discount.discount_amount = discount_data.discount_amount
        discount.is_active = discount_data.is_active
        discount.start_at = discount_data.start_at
        discount.end_at = discount_data.end_at

        created_discount = await self.repository.create(discount)
        return MODEL_MAP[discount_data.discount_type].model_validate(created_discount)


    # ---------------- Update ----------------
    async def update(self, id: UUID, update_data: DiscountUpdate, type: Discount_Model_Type) -> DiscountRead:
        discount = await self.repository.get_discount_by_id(id, type)
        if discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(discount, field, value)

        updated_discount = await self.repository.update(discount)
        return MODEL_MAP[type].model_validate(updated_discount)


    # ---------------- Delete ----------------
    async def delete(self, id: UUID, type: Discount_Model_Type) -> bool:
        result = await self.repository.delete(id, type)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return result


    # ---------------- Set Status ----------------
    async def set_discount_status(self, id: UUID, discount_status: DiscountSetStatus, type: Discount_Model_Type) -> bool:
        result = await self.repository.set_discount_status(id, discount_status, type)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found or you enterd the same status")
        return result


