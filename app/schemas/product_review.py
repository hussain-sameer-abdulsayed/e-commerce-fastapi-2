from __future__ import annotations
from typing import Optional

from pydantic import Field
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID



class ProductReviewBase(BaseSchemaConfig):
   rating: int = Field(ge=1, le=5)
   comment: Optional[str] = None



class ProductReviewCreate(ProductReviewBase):
   user_profile_id: UUID
   product_id: UUID


class ProductReviewUpdate(BaseSchemaConfig):
   rating : Optional[int] = Field(None, ge=1, le=5)
   comment: Optional[str] = None

class ProductReviewRead(ProductReviewBase, BaseSchema):
   user_profile_id: UUID
   product_id: UUID
   is_approved: bool





      