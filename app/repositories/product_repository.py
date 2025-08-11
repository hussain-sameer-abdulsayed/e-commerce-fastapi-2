from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models.category import Category
from app.models.product import Product
from .category_repository import CategoryRepository

category_repository = CategoryRepository()

class ProductRepository:
   def __init__(self, db: AsyncSession):
      self.db = db

   async def get_all(self, only_available: bool =False) -> List[Product]:
      statement = select(Product).order_by(Product.name)
      if only_available:
         statement = statement.where(Product.is_available == True)
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_id(self, id: UUID) -> Optional[Product]:
      statement = select(Product).where(Product.id == id)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_with_categories(self, id: UUID) -> Optional[Product]:   
      statement = (
         select(Product)
         .options(selectinload(Product.categories))
         .where(Product.id == id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_by_name(self, name: str) -> Optional[Product]:
      statement = select(Product).where(Product.name == name)
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_by_category_id(self, category_id: UUID, only_available: bool = False) -> List[Product]:
      statement = (
         select(Product)
         .join(Product.categories)
         .where(Product.categories.any(id=category_id))
         .order_by(Product.name)
      )
      if only_available:
         statement = statement.where(Product.is_available == True)

      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_by_seller_id(self, seller_id: UUID, only_available: bool = False) -> List[Product]:
      statement = (
         select(Product)
         .where(Product.seller_profile_id == seller_id)
         .order_by(Product.name)
      )
      if only_available:
         statement = statement.where(Product.is_available == True)

      result = await self.db.execute(statement)
      return list(result.scalars().all())
   

   async def search(self, text: str, only_available: bool = False) -> List[Product]:
      statement = (
         select(Product)
         .where(
            or_(
               Product.name.ilike(f"%{text}%"),
               Product.description.ilike(f"%{text}%")
            )
         )
         .order_by(Product.name)
      )
      if only_available:
         statement = statement.where(Product.is_available == True)

      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def full_text_search(self, search_text: str, only_available: bool =False) -> List[Product]:
        # Prepare the search term for prefix matching
        search_terms = " & ".join(
            f"{term}:*" for term in search_text.strip().split()
        )
        statement = (
            select(Product)
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
        if only_available:
         statement = statement.where(Product.is_available == True) 

        result = await self.db.execute(statement)
        return list(result.scalars().all())


   async def create(self, product: Product) -> Product:

      self.db.add(product)
      await self.db.execute()
      await self.db.refresh(product)
      return product


   async def update(self, product: Product) -> Product:
      product.updated_at = datetime.utcnow()
      self.db.add(product)
      await self.db.execute()
      await self.db.refresh(product)
      return product
   

   async def delete(self, id: UUID) -> bool:
      product = await self.get_by_category_id(id)
      if product:
         await self.db.delete(product)
         await self.db.commit()
         return True
      return False


   async def exists_by_name(self, name: str, exclude_id: Optional[UUID] = None) -> bool:
      statement = select(Product).where(Product.name == name)
      if exclude_id:
         statement = statement.where(Product.id != exclude_id)

      result = await self.db.execute(statement)
      product = result.first()
      return product is not None





