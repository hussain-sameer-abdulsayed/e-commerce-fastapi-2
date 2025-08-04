from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession




from app.services.category_service import CategoryService
from database import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


router = APIRouter(
   prefix="/categories",
   tags=["categories"],
   responses={404: {"description": "Not found"}}
)

async def get_category_service(db:AsyncSession = Depends(get_db)) -> CategoryService:
   return CategoryService(db)




@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
      category: CategoryCreate,
      service: CategoryService = Depends(get_category_service)
):
   return await service.create(category)


@router.get("/", response_model= List[CategoryRead])
async def get_categories(
      service: CategoryService = Depends(get_category_service)
):
   return await service.get_all()