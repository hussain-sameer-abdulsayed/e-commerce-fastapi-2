


from typing import Optional
from uuid import UUID
from pydantic import Field
from app.schemas.base_schema import BaseSchema, BaseSchemaConfig


class ImageBase(BaseSchemaConfig):
   file_name: str
   original_file_name: str
   file_path: str
   file_size: int = Field(ge=0, description="File size in bytes") # in bytes
   mime_type: str
   product_id: Optional[UUID] = None
   category_id: Optional[UUID] = None
   seller_profile_id: Optional[UUID] = None
   user_profile_id: Optional[UUID] = None


class ImageCreate(ImageBase):
   pass

### for now no image update 
class ImageUpdate(BaseSchemaConfig):
   pass

class ImageRead(ImageBase, BaseSchema):
   pass


