from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import text, or_
from app.models.category import Category



class CategoryRepository:
   def __init__(self, db: AsyncSession):
      self.db = db
   

   async def get_by_id(self, id:UUID) -> Optional[Category]:
      statement = select(Category).where(Category.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_name(self, name: str) -> Optional[Category]:
      statement = select(Category).where(Category.name == name)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_all(self) -> List[Category]:
      statement = select(Category).order_by(Category.name)
      result = await self.db.execute(statement)
      return list(result.scalars().all())
   

   async def get_all_with_products(self) -> List[Category]:
      statement = (
         select(Category)
         .options(selectinload(Category.products))
         .order_by(Category.name)
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_with_products(self, category_id: UUID) -> Optional[Category]:
    statement = (
        select(Category)
        .options(selectinload(Category.products))
        .where(Category.id == category_id)
    )
    result = await self.db.execute(statement)
    return result.scalar_one_or_none()
   

   async def search_by_name(self, text: str) -> List[Category]:
      statement = (
         select(Category)
         .where(
            or_(
               Category.name.ilike(f"%{text}%"),
               Category.description.ilike(f"%{text}%")
            )
         )
         .order_by(Category.name)
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())
   

   async def full_text_search(self, search_text: str) -> List[Category]:
    # Prepare the search term for prefix matching
    search_terms = " & ".join(
        f"{term}:*" for term in search_text.strip().split()
    )

    statement = (
        select(Category)
        .where(
            text("""
                to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))
                @@ to_tsquery('english', :search)
            """)
        )
        .params(search=search_terms)
        .order_by(
            text("""
                ts_rank(
                    to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, '')),
                    to_tsquery('english', :search)
                ) DESC
            """)
        )
    )

    result = await self.db.execute(statement)
    return list(result.scalars().all())


   async def create(self, category:Category) -> Category:
      self.db.add(category)
      await self.db.commit()
      await self.db.refresh(category)
      return category


   async def update(self, category: Category) -> Category:
      category.updated_at = datetime.utcnow()
      self.db.add(category)
      await self.db.commit()
      await self.db.refresh(category)
      return category
   

   async def delete(self, id: UUID) -> bool:
      category = await self.get_by_id(id)
      if category:
         await self.db.delete(category)
         await self.db.commit()
         return True
      return False
      

   async def exists_by_name(self, name: str, exclude_id: Optional[UUID] = None) -> bool:
      statement = select(Category).where(Category.name == name)
      if exclude_id:
         statement = statement.where(Category.id != exclude_id)
         
      result = await self.db.execute(statement)
      category = result.first()
      return category is not None



   