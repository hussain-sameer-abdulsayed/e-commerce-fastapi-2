from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import text
from .base_repository import BaseRepository
from app.models.category import Category



class CategoryRepository(BaseRepository[Category]):
   def __init__(self, db: AsyncSession):
      super().__init__(Category, db)
   

   async def get_by_name(self, name: str) -> Optional[Category]:
      statement = select(Category).where(Category.name == name)
      result = await self.db.exec(statement)
      return result.first()
   

   async def get_with_products(self, category_id: UUID) -> Optional[Category]:
    statement = (
        select(Category)
        .options(selectinload(Category.products))
        .where(Category.id == category_id)
    )
    result = await self.db.execute(statement)
    return result.scalars().first()


   async def search_by_name(self, name: str) -> List[Category]:
      statement = (
         select(Category)
         .where(Category.name.ilike(f"%{name}%"))
         .order_by(Category.name)
      )
      result = await self.db.execute(statement)
      return result.scalars().all()
   

   async def update_category(self, category_id: UUID, update_data: dict) -> Optional[Category]:
      category = await self.get_by_id(category_id)
      if not category:
         return None
      
      update_data["updated_at"] = datetime.utcnow()

      for field, value in update_data.items():
         if hasattr(category, field) and value is not None:
            setattr(category, field, value)

      self.db.add(category)
      await self.db.commit()
      await self.db.refresh(category)
      return category
   

   async def full_text_search(self, search_text: str) -> List[Category]:
      statement = (
            select(Category)
            .where(
                text("to_tsvector('english', name || ' ' || description) @@ plainto_tsquery('english', :search)")
            )
            .params(search=search_text)
            .order_by(text("ts_rank(to_tsvector('english', name || ' ' || description), plainto_tsquery('english', :search)) DESC"))
      )
      result = await self.db.execute(statement)
      return result.scalars().all()
   

   