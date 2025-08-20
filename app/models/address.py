
from sqlmodel import Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

# Import enum properly
from app.enums.enums import Province
from app.models.base_model import BaseModel

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.models import Order, SellerProfile, User


class AddressBase(BaseModel, table=False):
    # Fix: Use proper enum field definition
    province: Province = Field(default=Province.BAGHDAD)
    city: str
    street: str
    nearest_point: Optional[str] = None
    is_default: bool = Field(default=False)
    is_store_address: bool = Field(default=False)
    is_shipment_address: bool = Field(default=True)

    # Foreign key relationships
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", index=True)
    seller_profile_id: Optional[UUID] = Field(default=None, foreign_key="seller_profiles.id", index=True)


class Address(AddressBase, table=True):
    __tablename__ = "addresses" # type: ignore
    
    # Relationships - define these after the table model
    orders: List["Order"] = Relationship(back_populates="address")
    user: Optional["User"] = Relationship(back_populates="addresses")
    seller_profile: Optional["SellerProfile"] = Relationship(back_populates="addresses")

