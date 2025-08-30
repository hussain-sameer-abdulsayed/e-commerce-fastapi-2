
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import uuid
from fastapi import HTTPException, status, UploadFile

from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.schemas.image import ImageRead
from app.services.image_service import ImageService


router = APIRouter(
   responses= {404: {"description":"Not found"}}
)


async def get_image_service(db: AsyncSession = Depends(get_db)) -> ImageService:
   return ImageService(db)


@router.get("/entity/{entity_type}/{entity_id}", response_model= List[ImageRead], status_code= status.HTTP_200_OK)
async def get_images_by_entity(
   entity_id: UUID,
   entity_type: str,
   service: ImageService = Depends(get_image_service)
):
   return await service.get_images_by_entity(entity_type, entity_id)


@router.get("/{image_id}", response_model= ImageRead, status_code= status.HTTP_200_OK)
async def get_image_by_id(
   image_id: UUID,
   service: ImageService = Depends(get_image_service)
):
   return await service.get_image_by_id(image_id)


@router.delete("/{image_id}", response_model=ImageRead, status_code=status.HTTP_200_OK)
async def delete_image_by_id(
   image_id: UUID,
   service: ImageService = Depends(get_image_service)
):
   return await service.delete(image_id)




