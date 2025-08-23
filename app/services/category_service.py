from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func


from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryWithProducts
from app.models.user import User


class CategoryService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = CategoryRepository(db)


   async def get_all_categories(self) -> List[CategoryRead]:
      categories = await self.repository.get_all()
      return [CategoryRead.model_validate(category) for category in categories]
   

   async def get_all_categories_with_products(self) -> List[CategoryWithProducts]:
      categories = await self.repository.get_all_with_products()
      return [CategoryWithProducts.model_validate(category) for category in categories]


   async def get_category_by_id(self, category_id: UUID, inclue_products: bool = False) -> CategoryRead | CategoryWithProducts:
      if inclue_products:
         category = await self.repository.get_with_products(category_id)
         if not category:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Category not found"
            )
         return CategoryWithProducts.model_validate(category)

      else:
         category = await self.repository.get_by_id(category_id)
         if not category:
            raise HTTPException(
               status_code= status.HTTP_404_NOT_FOUND,
               detail="Category not found"
            )
         return CategoryRead.model_validate(category)
      

   async def get_category_by_name(self, category_name: str) -> CategoryRead:
      category = await self.repository.get_by_name(category_name)
      if not category:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
         )
      
      return CategoryRead.model_validate(category)


   async def search_categories(self, search_text: str, use_full_text: bool=False) -> List[CategoryRead]:
      if not search_text.strip():
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "please enter a text"
         )
      
      search_text = search_text.strip()

      if use_full_text:
         try:
            categories = await self.repository.full_text_search(search_text)
         except:
            # Fallback to ILIKE search if full-text search fails
            categories = await self.repository.search(search_text)

      else:
         categories = await self.repository.search(search_text)
      

      return [CategoryRead.model_validate(category) for category in categories]

   
   async def create_category(self, user_id: UUID, category_data: CategoryCreate) -> CategoryRead:


      if user_id:
         user = await self.db.get(User, user_id)
         if not user:
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="User does not exist"
                )



      # check category name if exists
      if await self.repository.exists_by_name(category_data.name):
         raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= f"Category with name '{category_data.name}' already exists"
            )
      # create category
      category = Category(**category_data.model_dump())

      ## save to database
      created_category = await self.repository.create(category)

      return CategoryRead.model_validate(created_category) 


   async def update_category(self, category_id:UUID, update_data: CategoryUpdate) -> CategoryRead:
      category = await self.repository.get_by_id(category_id)
      if not category:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Category not found"
         )
      
      update_dict = update_data.model_dump(exclude_unset= True)
      if "name" in update_dict and update_dict["name"] != category.name:
         exists = await self.repository.exists_by_name(update_dict["name"], exclude_id= category_id)
         if exists:
            raise HTTPException(
               status_code= status.HTTP_409_CONFLICT,
               detail= f"Category with name {update_dict['name']} already exists"
            )

      ## update fields
      for field, value in update_dict.items():
         if hasattr(category, field) and value is not None:
            setattr(category, field, value)

      # save updates
      updated_category = await self.repository.update(category)

      return CategoryRead.model_validate(updated_category)
   

   async def delete_category(self, category_id: UUID) -> bool:
      result = await self.repository.delete(category_id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Category not found"
         )

      return result

