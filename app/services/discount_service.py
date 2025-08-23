from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.enums import Discount_Model_Type
from app.models import CategoryDiscount, ProductDiscount
from app.models.shipment_discount import ShipmentDiscount
from app.repositories import CategoryRepository, ProductRepository, ShipmentRepository, DiscountRepository

from app.schemas.base_schema import DiscountSetStatus
from schemas import CategoryDiscountCreate, CategoryDiscountRead, CategoryDiscountUpdate, ProductDiscountCreate, ProductDiscountRead, ProductDiscountUpdate, ShipmentDiscountCreate, ShipmentDiscountRead, ShipmentDiscountUpdate



class DiscountService:
   def __init__(self, db: AsyncSession) -> None:
      self.db = db
      self.repository = DiscountRepository(db)
      self.category_repository = CategoryRepository(db)
      self.product_repository = ProductRepository(db)
      self.shipment_repository = ShipmentRepository(db)


   async def get_all(self, type: Discount_Model_Type) -> List[CategoryDiscountRead] | List[ProductDiscountRead] | List[ShipmentDiscountRead]:
      discounts = await self.repository.get_all(type)
      if type == Discount_Model_Type.CATEGORY:
         discounts_read = [CategoryDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.PRODUCT:
         discounts_read = [ProductDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.SHIPMENT:
         discounts_read = [ShipmentDiscountRead.model_validate(dis) for dis in discounts]
      
      return discounts_read


   async def get_by_active_status(self, type: Discount_Model_Type, is_active: bool) -> List[CategoryDiscountRead] | List[ProductDiscountRead] | List[ShipmentDiscountRead]:
      discounts = await self.repository.get_by_active_status(type, is_active)
      if type == Discount_Model_Type.CATEGORY:
         discounts_read = [CategoryDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.PRODUCT:
         discounts_read = [ProductDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.SHIPMENT:
         discounts_read = [ShipmentDiscountRead.model_validate(dis) for dis in discounts]
      
      return discounts_read


   async def get_discount_by_id(self, id: UUID, type: Discount_Model_Type) -> Optional[CategoryDiscountRead] | Optional[ProductDiscountRead] | Optional[ShipmentDiscountRead]:
      discount = await self.repository.get_discount_by_id(id, type)
      if type == Discount_Model_Type.CATEGORY:
         discounts_read = CategoryDiscountRead.model_validate(discount)
      elif type == Discount_Model_Type.PRODUCT:
        discounts_read = ProductDiscountRead.model_validate(discount)
      elif type == Discount_Model_Type.SHIPMENT:
         discounts_read = ShipmentDiscountRead.model_validate(discount)
      
      return discounts_read


   async def get_discounts_by_entity_id(self, id: UUID, type: Discount_Model_Type) -> List[CategoryDiscountRead] | List[ProductDiscountRead] | List[ShipmentDiscountRead]:
      discounts = await self.repository.get_discounts_by_entity_id(id, type)
      if type == Discount_Model_Type.CATEGORY:
         discounts_read = [CategoryDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.PRODUCT:
         discounts_read = [ProductDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.SHIPMENT:
         discounts_read = [ShipmentDiscountRead.model_validate(dis) for dis in discounts]
      
      return discounts_read


   async def get_active_discounts_by_entity_id(self, id: UUID, type: Discount_Model_Type) -> List[CategoryDiscountRead] | List[ProductDiscountRead] | List[ShipmentDiscountRead]:
      discounts = await self.repository.get_active_discounts_by_entity_id(id, type)
      if type == Discount_Model_Type.CATEGORY:
         discounts_read = [CategoryDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.PRODUCT:
         discounts_read = [ProductDiscountRead.model_validate(dis) for dis in discounts]
      elif type == Discount_Model_Type.SHIPMENT:
         discounts_read = [ShipmentDiscountRead.model_validate(dis) for dis in discounts]
      
      return discounts_read


   async def create(self, discount_data: CategoryDiscountCreate | ProductDiscountCreate | ShipmentDiscountCreate) -> CategoryDiscountRead | ProductDiscountRead | ShipmentDiscountRead:
      if discount_data.discount_type == Discount_Model_Type.CATEGORY:
         exists = await self.category_repository.get_by_id(discount_data.entity_id)
         if not exists:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= "Category not found"
            )
         discount = CategoryDiscount(**discount_data.model_dump(exclude_unset= True))
         created_discount = await self.repository.create(discount)

         return CategoryDiscountRead.model_validate(created_discount)


      elif discount_data.discount_type == Discount_Model_Type.PRODUCT:
         exists = await self.product_repository.get_by_id(discount_data.entity_id)
         if not exists:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= "Product not found"
            )
         discount = ProductDiscount(**discount_data.model_dump(exclude_unset= True))
         created_discount = await self.repository.create(discount)

         return ProductDiscountRead.model_validate(created_discount)


      elif discount_data.discount_type == Discount_Model_Type.SHIPMENT:
         exists = await self.shipment_repository.get_by_id(discount_data.entity_id)
         if not exists:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= "Shipment not found"
            )
      discount = ShipmentDiscount(**discount_data.model_dump(exclude_unset= True))
      created_discount = await self.repository.create(discount)

      return ShipmentDiscountRead.model_validate(created_discount)


   async def update(self, id: UUID, update_data: CategoryDiscountUpdate | ProductDiscountUpdate | ShipmentDiscountUpdate, type: Discount_Model_Type) -> CategoryDiscountRead | ProductDiscountRead | ShipmentDiscountRead:
      discount = await self.repository.get_discount_by_id(id, type)
      if not discount:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Discount not found"
         )
      
      update_dict = update_data.model_dump(exclude_unset= True)

      for field, value in update_dict.items():
         if hasattr(discount, field) and value is not None:
            setattr(discount, field, value)
      
      updated_discount = await self.repository.update(discount)

      if type == Discount_Model_Type.CATEGORY:
         return CategoryDiscountRead.model_validate(updated_discount)

      elif type == Discount_Model_Type.PRODUCT:
         return ProductDiscountRead.model_validate(updated_discount)

      elif type == Discount_Model_Type.SHIPMENT:
         return ShipmentDiscountRead.model_validate(updated_discount)


   async def delete(self, id: UUID, type: Discount_Model_Type) -> bool:
      result = await self.repository.delete(id, type)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Discount not found"
         )
      return result


   async def set_discount_status(self, id: UUID, discount_statu: DiscountSetStatus, type: Discount_Model_Type) -> bool:
      result = await self.repository.set_discount_status(id, discount_statu, type)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Discount not found"
         )
      return True

