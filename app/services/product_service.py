
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession



from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductWithCategories
from app.repositories.product_repository import ProductRepository



class ProductService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = ProductRepository(db)



   async def get_all_products(self, only_available: Optional[bool] =False) -> List[ProductRead]:
      products = await self.repository.get_all(only_available)
      return [ProductRead.model_validate(product) for product in products]


   async def get_by_id(self, id: UUID, include_categories: bool = False) -> ProductRead | ProductWithCategories:
      if include_categories:
         product = await self.repository.get_with_categories(id)
         if not product:
            raise HTTPException(
               status_code= status.HTTP_404_NOT_FOUND,
               detail="Product not found"
            )
         return ProductWithCategories.model_validate(product)
      else:
         product = await self.repository.get_by_id(id)
         if not product:
            raise HTTPException(
               status_code= status.HTTP_404_NOT_FOUND,
               detail="Product not found"
            )
         return ProductRead.model_validate(product)





