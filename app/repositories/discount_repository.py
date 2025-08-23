from datetime import datetime
from gc import disable
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from app.enums.enums import Discount_Model_Type
from app.models.category_discount import CategoryDiscount
from app.models.product_discount import ProductDiscount
from app.models.shipment_discount import ShipmentDiscount
from app.schemas.base_schema import DiscountSetStatus


class DiscountRepository:
   def __init__(self, db:AsyncSession):
      self.db = db

   
   async def get_all(self, type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).order_by(desc(CategoryDiscount.created_at))
      elif type == Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).order_by(desc(ProductDiscount.created_at))
      elif type == Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())

   
   async def get_by_active_status(self, type: Discount_Model_Type, is_active: bool) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      now = datetime.now()
      if type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).order_by(desc(CategoryDiscount.created_at))
         if is_active:
            
            statement = statement.where(CategoryDiscount.is_active == True and CategoryDiscount.start_at <= now and CategoryDiscount.end_at >= now)
         else:
            statement = statement.where(CategoryDiscount.is_active == False and CategoryDiscount.start_at > now and CategoryDiscount.end_at < now)

      elif type == Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).order_by(desc(ProductDiscount.created_at))
         if is_active:
            statement = statement.where(ProductDiscount.is_active == True and ProductDiscount.start_at <= now and ProductDiscount.end_at >= now)
         else:
            statement = statement.where(ProductDiscount.is_active == False and CategoryDiscount.start_at > now and CategoryDiscount.end_at < now)

      elif type == Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).order_by(desc(ShipmentDiscount.created_at))
         if is_active:
            statement = statement.where(ShipmentDiscount.is_active == True and ShipmentDiscount.start_at <= now and ShipmentDiscount.end_at >= now)
         else:
            statement = statement.where(ShipmentDiscount.is_active == False and ShipmentDiscount.start_at > now and ShipmentDiscount.end_at < now)
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_discount_by_id(self, id:UUID, type: Discount_Model_Type) -> Optional[CategoryDiscount] | Optional[ProductDiscount] | Optional[ShipmentDiscount]:
      if type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.id == id).order_by(desc(CategoryDiscount.created_at))
      elif type == Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.id == id).order_by(desc(ProductDiscount.created_at))
      elif type == Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.id == id).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   
## ex get category discounts for a spesefic category by category id
   async def get_discounts_by_entity_id(self, id:UUID, type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.category_id == id).order_by(desc(CategoryDiscount.created_at))
      elif type == Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.product_id == id).order_by(desc(ProductDiscount.created_at))
      elif type == Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.shipment_id == id).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())

## ex get category active discounts for a spesefic category by category id
   async def get_active_discounts_by_entity_id(self, id:UUID, type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.category_id == id and CategoryDiscount.is_active == True).order_by(desc(CategoryDiscount.created_at))
      elif type == Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.product_id == id and ProductDiscount.is_active == True).order_by(desc(ProductDiscount.created_at))
      elif type == Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.shipment_id == id and ShipmentDiscount.is_active == True).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def create(self, discount: ProductDiscount | CategoryDiscount | ShipmentDiscount) -> ProductDiscount | CategoryDiscount | ShipmentDiscount:
      self.db.add(discount)
      await self.db.commit()
      await self.db.refresh(discount)

      return discount
   

   async def update(self, discount: ProductDiscount | CategoryDiscount | ShipmentDiscount) -> ProductDiscount | CategoryDiscount | ShipmentDiscount:
      discount.updated_at = datetime.utcnow()
      self.db.add(discount)
      await self.db.commit()
      await self.db.refresh(discount)

      return discount


   async def delete(self, id: UUID, type: Discount_Model_Type) -> bool:
      discount = await self.get_discount_by_id(id, type)
      if not discount:
         return False
      
      await self.db.delete(discount)
      await self.db.commit()

      return True


   async def set_discount_status(self, id: UUID, status: DiscountSetStatus, type: Discount_Model_Type) -> bool:
      discount = await self.get_discount_by_id(id, type)
      if not discount or discount.is_active == status.is_active:
         return False
      
      discount.is_active = status.is_active
      self.db.add(discount)
      await self.db.commit()
      
      return True

