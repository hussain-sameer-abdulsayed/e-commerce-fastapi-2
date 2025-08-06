from __future__ import annotations
from fastapi import HTTPException, APIRouter, Depends, Query, status
from app.services.category_service import CategoryService
from app.db.database import get_db
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(
   responses={404: {"description": "Not found"}}
)


async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
   return CategoryService(db)


@router.get("/", response_model=List[CategoryRead], status_code= status.HTTP_200_OK)
async def get_categories(
    search: str = Query(None, description="search by name"),
    service: CategoryService = Depends(get_category_service)
):
    if search:
        return await service.search_categories(search)
    return await service.get_all_categories()


@router.get("/search", response_model=List[CategoryRead], status_code=status.HTTP_200_OK)
async def search_categories(
    q: str = Query(..., min_length=1, description="Search categories"),
    full_text: bool = Query(False, description="Use full text search"),
    service: CategoryService = Depends(get_category_service)
):
    return await service.search_categories(q, full_text)


@router.get("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
async def get_category(
    category_id: UUID,
    include_products: bool = Query(False, description="Include products in response"),
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_id(category_id, include_products)


@router.get("/name/{category_name}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
async def get_category_by_name(
    category_name: str,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_name(category_name)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.create_category(category.created_by_id, category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id : UUID,
    service : CategoryService = Depends(get_category_service)
):
    success = await service.delete_category(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )


@router.put("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_202_ACCEPTED)
async def update_category(
    category_id: UUID,
    category_update: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.update_category(category_id, category_update)

