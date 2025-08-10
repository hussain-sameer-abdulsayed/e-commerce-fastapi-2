from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchema
from uuid import UUID



class ProductReviewBase(BaseSchema):
   rating: int
   comment: Optional[str] = None



class ProductReviewCreate(ProductReviewBase):
   user_profile_id: UUID
   product_id: UUID


class ProductReviewUpdate(BaseSchema):
   rating : Optional[int] = None
   comment: Optional[str] = None

class ProductReviewRead(ProductReviewBase):
   id: UUID
   user_profile_id: UUID
   product_id: UUID
   is_approved: bool
   created_at: datetime
   updated_at: datetime





      