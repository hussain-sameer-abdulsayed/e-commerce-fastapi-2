import os
from typing import List
from uuid import UUID
import uuid
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ALLOWED_MIME_TYPES, UPLOAD_DIRECTORY, MAX_FILE_SIZE, MAX_IMAGES_PER_PRODUCT, ALLOWED_ENTITES
from app.models.image import Image
from app.repositories.image_repository import ImageRepository
from app.schemas.image import ImageCreate, ImageRead

class ImageService:
   def __init__(self, db: AsyncSession) -> None:
      self.db = db
      self.repository = ImageRepository(db)
      self.upload_directory = UPLOAD_DIRECTORY
      self.allowed_mime_types = ALLOWED_MIME_TYPES
      self.max_file_size = MAX_FILE_SIZE
      self.max_images_per_product = MAX_IMAGES_PER_PRODUCT
      self.allowed_entites = ALLOWED_ENTITES

      # Ensure upload directory exists
      os.makedirs(self.upload_directory, exist_ok= True)


   def _validate_image_file(self, file: UploadFile) -> None:
      if file.size and file.size > self.max_file_size:
         raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size too large. Maximum allowed: {self.max_file_size / (1024*1024):.1f}MB"
            )
      if file.content_type not in self.allowed_mime_types:
         raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(self.allowed_mime_types)}"
            )


   async def get_image_by_id(self, image_id: UUID) -> ImageRead:
      image = await self.repository.get_by_id(image_id)
      if not image:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Image not found"
         )
      return ImageRead.model_validate(image)


   async def get_images_by_entity(self, entity_type: str, entity_id: UUID) -> List[ImageRead]:
      images = await self.repository.get_by_entity(entity_type, entity_id)
      return [ImageRead.model_validate(image) for image in images]


   async def upload_images(
         self, 
         files: List[UploadFile],
         entity_type: str,
         entity_id: UUID
         ) -> List[ImageRead]:
      
      if entity_type not in self.allowed_entites:
         raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid entity type. Must be one of: {', '.join(self.allowed_entites)}"
            )

      if entity_type == "product":
         existing_count = await self.repository.count_images_by_product(entity_id)
         if existing_count + len(files) > self.max_images_per_product:
            raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= f"Maximum {self.max_images_per_product} images allowed per product"
            )
         
      uploaded_imaegs = []

      for i, file in enumerate(files):
         # Validate file
         self._validate_image_file(file)

         # Generate unique filename
         file_extension = os.path.splitext(file.filename)[1] # type: ignore
         unique_file_name = f"{uuid.uuid4().hex}{file_extension}"
         file_path = os.path.join(self.upload_directory, unique_file_name)

         # Save file
         try:
            with open(file_path, "wb") as buffer:
               content = await file.read()
               buffer.write(content)

            # Create image record
            image_data = Image(
               file_name= unique_file_name,
               original_file_name= file.filename or "unknown",
               file_path= file_path,
               file_size= len(content),
               mime_type= file.content_type or "image/png" ## default one
            )

            # Set entity relationship
            if entity_type == "category":
               image_data.category_id = entity_id
            elif entity_type == "product":
               image_data.product_id = entity_id
            elif entity_type == "user_profile":
               image_data.user_profile_id = entity_id
            elif entity_type == "seller_profile":
               image_data.seller_profile_id = entity_id
            
            # Save to database
            image = await self.repository.create(image_data)
            uploaded_imaegs.append(ImageRead.model_validate(image))

         except Exception as e:
            # Clean up file if database save fails
            if os.path.exists(file_path):
               os.remove(file_path)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to save image: {str(e)}"
                )

      return uploaded_imaegs


   async def delete(self, image_id: UUID) -> bool:
      image = await self.repository.get_by_id(image_id)
      if not image:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
      # Delete file from filesystem
      if os.path.exists(image.file_path):
         try:
            os.remove(image.file_path)
         except Exception:
            pass  # Continue even if file deletion fails

      # Delete from database
      return await self.repository.delete(image_id)

