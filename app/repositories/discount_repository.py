from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

from app.enums.enums import Discount_Model_Type
from app.models.category_discount import CategoryDiscount
from app.models.product_discount import ProductDiscount
from app.models.shipment_discount import ShipmentDiscount


class DiscountRepository:
   def __init__(self, db:AsyncSession):
      self.db = db

   
   async def get_all(self,type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if Discount_Model_Type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).order_by(desc(CategoryDiscount.created_at))
      elif Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).order_by(desc(ProductDiscount.created_at))
      elif Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())

   
   async def get_by_active_status(self,type: Discount_Model_Type, is_active: bool) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if Discount_Model_Type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).order_by(desc(CategoryDiscount.created_at))
         if is_active:
            statement = statement.where(CategoryDiscount.is_active == True)
         else:
            statement = statement.where(CategoryDiscount.is_active == False)

      elif Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).order_by(desc(ProductDiscount.created_at))
         if is_active:
            statement = statement.where(ProductDiscount.is_active == True)
         else:
            statement = statement.where(ProductDiscount.is_active == False)

      elif Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).order_by(desc(ShipmentDiscount.created_at))
         if is_active:
            statement = statement.where(ShipmentDiscount.is_active == True)
         else:
            statement = statement.where(ShipmentDiscount.is_active == False)
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_discount_by_id(self, id:UUID, type: Discount_Model_Type) -> Optional[CategoryDiscount] | Optional[ProductDiscount] | Optional[ShipmentDiscount]:
      if Discount_Model_Type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.id == id).order_by(desc(CategoryDiscount.created_at))
      elif Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.id == id).order_by(desc(ProductDiscount.created_at))
      elif Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.id == id).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   
## ex get category discounts for a spesefic category by category id
   async def get_discounts_by_type_id(self, id:UUID, type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if Discount_Model_Type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.category_id == id).order_by(desc(CategoryDiscount.created_at))
      elif Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.product_id == id).order_by(desc(ProductDiscount.created_at))
      elif Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.shipment_id == id).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())

## ex get category active discounts for a spesefic category by category id
   async def get_active_discounts_by_type_id(self, id:UUID, type: Discount_Model_Type) -> List[CategoryDiscount] | List[ProductDiscount] | List[ShipmentDiscount]:
      if Discount_Model_Type == Discount_Model_Type.CATEGORY:
         statement = select(CategoryDiscount).where(CategoryDiscount.category_id == id and CategoryDiscount.is_active == True).order_by(desc(CategoryDiscount.created_at))
      elif Discount_Model_Type.PRODUCT:
         statement = select(ProductDiscount).where(ProductDiscount.product_id == id and ProductDiscount.is_active == True).order_by(desc(ProductDiscount.created_at))
      elif Discount_Model_Type.SHIPMENT:
         statement = select(ShipmentDiscount).where(ShipmentDiscount.shipment_id == id and ShipmentDiscount.is_active == True).order_by(desc(ShipmentDiscount.created_at))
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())
