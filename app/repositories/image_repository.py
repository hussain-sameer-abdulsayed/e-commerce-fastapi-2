from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.image import Image


class ImageRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_by_id(self, image_id: UUID) -> Optional[Image]:
      statement = select(Image).where(Image.id == image_id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[Image]:
      if entity_type == "category":
         statement = select(Image).where(Image.category_id == entity_id)
      elif entity_type == "product":
         statement = select(Image).where(Image.product_id == entity_id)
      elif entity_type == "user_profile":
         statement = select(Image).where(Image.user_profile_id == entity_id)
      elif entity_type == "seller_profile":
         statement = select(Image).where(Image.seller_profile_id == entity_id)
      else:
         return []
      
      result = await self.db.execute(statement)
      return list(result.scalars().all())

   async def create(self, image: Image) -> Image:
      self.db.add(image)
      await self.db.commit()
      await self.db.refresh(image)
      return image


   async def update(self, image: Image) -> Image:
      self.db.add(image)
      await self.db.commit()
      await self.db.refresh(image)
      return image


   async def delete(self, image_id: UUID) -> bool:
      image = await self.get_by_id(image_id)
      if not image:
         return False
      await self.db.delete(image)
      await self.db.commit()
      return True


   async def count_images_by_product(self, product_id: UUID) -> int:
      statement = select(Image).where(Image.product_id == product_id)
      result = await self.db.execute(statement)
      return len(list(result.scalars().all()))


