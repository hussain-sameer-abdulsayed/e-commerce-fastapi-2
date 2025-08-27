
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import or_, text


from app.models.product import Product
from app.models.seller_profile import SellerProfile
from app.repositories.seller_profile_repository import SellerProfileRepository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductWithCategories
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository



class ProductService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = ProductRepository(db)
      self.category_repository = CategoryRepository(db)
      self.seller_profile_repository = SellerProfileRepository(db)



   async def get_all_products(self, only_available: bool =False) -> List[ProductRead]:
      products = await self.repository.get_all(only_available)
      if not products:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "There are no products"
         )
      return [ProductRead.model_validate(product) for product in products]


   async def get_product_by_id(self, id: UUID, include_categories: bool = False) -> ProductRead | ProductWithCategories:
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


   async def get_product_by_name(self, name: str) -> Optional[ProductRead]:
      product = await self.repository.get_by_name(name)
      if not product:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
         )
      return ProductRead.model_validate(product)


   async def get_products_by_category_id(self, category_id: UUID, only_available: bool = False) -> List[ProductRead]:
      products = await self.repository.get_by_category_id(category_id, only_available)
      
      if not products:
         raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "There are no products"
         )
      return [ProductRead.model_validate(product) for product in products]


   async def get_products_by_seller_id(self, seller_id: UUID, only_available: bool = False) -> List[ProductRead]:
      products = await self.repository.get_by_seller_id(seller_id, only_available)

      if not products:
         raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "There are no products"
         )
      return [ProductRead.model_validate(product) for product in products] 


   async def search_products(self, text: str, use_full_text: bool = False, only_available: bool = False) -> List[ProductRead]:
      if not text.strip():
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Please enter a text"
         )
      
      text = text.strip()

      if use_full_text:
         try:
            products = await self.repository.full_text_search(text, only_available)
         except:
            products = await self.repository.search(text, only_available)
      else:
         products = await self.repository.search(text, only_available)

      return [ProductRead.model_validate(product) for product in products]


   async def create_product(self, user_id: UUID, product_data: ProductCreate) -> ProductRead:


      if user_id:
         seller = await self.seller_profile_repository.get_by_user_id(user_id)
         if not seller:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail="Seller profile not found"
            )
      
      if product_data.category_ids:
         categories = await self.category_repository.get_by_ids(product_data.category_ids)

         if not categories or len(categories) != len(product_data.category_ids):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more categories not found"
            )

      product = Product(
         name = product_data.name,
         price= product_data.price,
         stock_quantity= product_data.stock_quantity,
         description= product_data.description,
         main_image_url= product_data.main_image_url,
         seller_profile_id= seller.id,
         categories= categories
      )

      new_product = await self.repository.create(product)
      return ProductRead.model_validate(new_product)


   async def delete_product(self, id: UUID) -> bool:
      result = await self.repository.delete(id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
         )
      
      return result


   async def update_product(
    self,
    user_id: UUID,
    product_id: UUID,
    update_data: ProductUpdate
) -> ProductRead:
    
    product = await self.repository.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
        )

    seller = await self.seller_profile_repository.get_by_user_id(user_id)
    if not seller or product.seller_profile_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seller profile not found, or does not belong to the seller"
        )

    # Check categories if provided
    if update_data.category_ids is not None:
        categories = await self.category_repository.get_by_ids(update_data.category_ids)
        if not categories or len(categories) != len(update_data.category_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more categories not found"
            )
        product.categories = categories

    update_dict = update_data.model_dump(exclude_unset=True)

    # Check unique name
    if "name" in update_dict and update_dict["name"] != product.name:
        if await self.repository.exists_by_name(update_dict["name"], exclude_id=product_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name {update_dict['name']} already exists"
            )

    # Update other fields
    for field, value in update_dict.items():
        if field != "category_ids" and hasattr(product, field) and value is not None:
            setattr(product, field, value)

    updated_product = await self.repository.update(product)
    return ProductRead.model_validate(updated_product)


