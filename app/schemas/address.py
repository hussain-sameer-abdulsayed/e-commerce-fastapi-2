from __future__ import annotations
from datetime import datetime
from typing import Optional
from .base_schema import BaseSchemaConfig, BaseSchema
from uuid import UUID
from app.enums.enums import Province



class AddressBase(BaseSchemaConfig):
    province: Province = Province.BAGHDAD
    city: str
    street: str
    nearest_point: Optional[str] = None
    is_default: bool = False  # Add default values
    is_store_address: bool = False
    is_shipment_address: bool = True


class AddressCreate(AddressBase):
   pass


class AddressUpdate(BaseSchemaConfig):
   province: Optional[Province] = None
   city: Optional[str] = None
   street: Optional[str] = None
   nearest_point: Optional[str] = None
   is_default: Optional[bool] = None
   is_store_address: Optional[bool] = None
   is_shipment_address: Optional[bool] = None


class AddressRead(AddressBase, BaseSchema):
   user_id : Optional[UUID] = None
   seller_profile_id: Optional[UUID] = None



