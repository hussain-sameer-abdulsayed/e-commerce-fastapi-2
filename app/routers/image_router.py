
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import uuid
from fastapi import File, HTTPException, status, UploadFile

from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.models.user import User
from app.schemas.image import ImageRead, ImageUpdate
from app.services.image_service import ImageService
from app.authentication.auth_dependency import(
    require_admin,
    require_seller,
    get_current_active_user
)


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


@router.post("/{entity_type}/{entity_id}", response_model= List[ImageRead], status_code= status.HTTP_200_OK)
async def upload_images(
   entity_type: str,
   entity_id: UUID,
   files: List[UploadFile] = File(..., description="Image files to upload"),
   service: ImageService = Depends(get_image_service),
   current_user: User = Depends(require_seller)
):
   if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
   
   if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 files allowed per upload"
        )
   
   return await service.upload_images(
       files,
       entity_type,
       entity_id
   )


@router.put("/{image_id}", response_model= ImageRead, status_code= status.HTTP_200_OK)
async def update_image_by_id(
    image_id: UUID,
    file: UploadFile,
    service: ImageService = Depends(get_image_service)
):
    return await service.update(image_id, file)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_by_id(
   image_id: UUID,
   service: ImageService = Depends(require_seller),
):
   return await service.delete(image_id)




