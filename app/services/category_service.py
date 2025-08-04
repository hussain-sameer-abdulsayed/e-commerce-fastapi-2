from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, func


from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from .base_service import BaseService



class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
   def __init__(self, db: AsyncSession):
      self.repository = CategoryRepository(db)
      super().__init__(self.repository)


   async def get_category_by_id(self, category_id: UUID, inclue_products: bool = False) -> CategoryRead:
      if inclue_products:
         category = await self.repository.get_with_products(category_id)
      else:
         category = await self.repository.get_by_id(category_id)

      if not category:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND
         )
      
      return CategoryRead.model_validate(category)
   

   async def search_category_by_name(self, search_text: str, use_full_text: bool=False) -> List[CategoryRead]:
      if not search_text.strip():
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST
         )
      
      search_text = search_text.strip()

      if use_full_text:
         try:
            categories = await self.repository.full_text_search(search_text)
         except:
            # Fallback to ILIKE search if full-text search fails
            categories = await self.repository.search_by_name(search_text)

      else:
         categories = await self.repository.search_by_name(search_text)
      

      return [CategoryRead.model_validate(category) for category in categories]
   

   async def update_category(self, category_id: UUID, category_data: CategoryUpdate) -> CategoryRead:
      existing_category = await self.repository.get_by_id(category_id)
      if not existing_category:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND   
         )
      
      if category_data.name and category_data.name != existing_category.name:
         name_conflict = await self.repository.get_by_name(category_data.name)
         if name_conflict:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail=f"Category with name '{category_data.name}' already exists"
            )
         
      update_data = category_data.model_dump(exclude_unset=True)
      updated_category = await self.repository.update_category(category_id, update_data)

      return CategoryRead.model_validate(updated_category)
   