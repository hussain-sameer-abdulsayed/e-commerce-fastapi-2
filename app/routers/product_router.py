from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends, Query, status
from app.db.database import get_db

from app.schemas.product import ProductRead, ProductCreate, ProductUpdate, ProductWithCategories
from app.services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
   responses={404: {"description": "Not found"}}
)


async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
   return ProductService(db)



@router.get("/", response_model=List[ProductRead], status_code= status.HTTP_200_OK)
async def get_products(
   search: Optional[str] = Query(None, description= "Search products"),
   only_available: bool = Query(False, description="True return only available products"),
   service: ProductService = Depends(get_product_service)
):
   if search:
      return await service.search_products(text= search, only_available= only_available)
   return await service.get_all_products(only_available= only_available)


@router.get("/search", response_model=List[ProductRead], status_code= status.HTTP_200_OK)
async def search_products(
   q: str = Query(..., min_length=1, description="Search products"),
   use_full_text: bool = Query(False, description="Use full text search algorithm"),
   only_available: bool = Query(False, description="True return only available products"),
   service: ProductService = Depends(get_product_service)
):
   return await service.search_products(text= q, use_full_text= use_full_text, only_available= only_available)


@router.get("/{product_id}", status_code= status.HTTP_200_OK)
async def get_product_by_id(
   product_id: UUID,
   include_categories: bool = Query(False, description= "including categories"),
   service: ProductService = Depends(get_product_service)
):
   return await service.get_product_by_id(product_id, include_categories = include_categories)


@router.get("/name/{product_name}", response_model= ProductRead, status_code= status.HTTP_200_OK)
async def get_product_by_name(
   product_name: str,
   service: ProductService = Depends(get_product_service)
):
   return await service.get_product_by_name(product_name)



@router.get("/category/{category_id}", response_model= List[ProductRead], status_code= status.HTTP_200_OK)
async def get_products_by_category_id(
   category_id: UUID,
   only_available: bool = Query(False, description="True return only available products"),
   service: ProductService = Depends(get_product_service)
):
   return await service.get_products_by_category_id(category_id= category_id, only_available= only_available)


@router.get("/seller/{seller_id}", response_model= List[ProductRead], status_code= status.HTTP_200_OK)
async def get_products_by_seller_id(
   seller_id: UUID,
   only_available: bool = Query(False, description="True return only available products"),
   service: ProductService = Depends(get_product_service)
):
   return await service.get_products_by_seller_id(seller_id= seller_id, only_available= only_available)


@router.post("/", response_model= ProductRead, status_code= status.HTTP_201_CREATED)
async def create_product(
   product: ProductCreate,
   service: ProductService = Depends(get_product_service)
):
   return await service.create_product(seller_id= product.seller_profile_id, product_data= product)


@router.put("/{product_id}", response_model= ProductRead, status_code= status.HTTP_200_OK)
async def update_product(
   product_id: UUID,
   seller_id: UUID,
   product_update: ProductUpdate,
   service: ProductService = Depends(get_product_service)
):
   return await service.update_product(seller_id= seller_id, product_id= product_id, update_data= product_update)


@router.delete("/{product_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_product(
   product_id: UUID,
   service: ProductService = Depends(get_product_service)
):
   return await service.delete_product(product_id)







