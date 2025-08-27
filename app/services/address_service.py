
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.models.seller_profile import SellerProfile
from app.models.user import User
from app.repositories.seller_profile_repository import SellerProfileRepository
from app.repositories.user_repository import UserRepository
from app.schemas.address import AddressCreate, AddressRead, AddressUpdate
from app.repositories.address_repository import AddressRepository




class AddressService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = AddressRepository(db)
      self.user_repository = UserRepository(db)
      self.seller_repository = SellerProfileRepository(db)
   

   async def get_all(self) -> List[AddressRead]:
      addresses = await self.repository.get_all()
      return [AddressRead.model_validate(address) for address in addresses]
   

   async def get_address(self, id: UUID) -> Optional[AddressRead]:
      address = await self.repository.get_address(id)
      if not address:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Address not found"
         )
      return AddressRead.model_validate(address)


   async def get_addresses_by_user_id(self, user_id: UUID) -> List[AddressRead]:
      addresses = await self.repository.get_addresses_by_user_id(user_id)
      return [AddressRead.model_validate(address) for address in addresses]


   async def get_addresses_by_seller_id(self, seller_id: UUID) -> List[AddressRead]:
      addresses = await self.repository.get_addresses_by_seller_id(seller_id)
      return [AddressRead.model_validate(address) for address in addresses]


   async def create(self, user_id: UUID, address_data: AddressCreate) -> AddressRead:
      if not address_data.is_store_address:
         user = await self.user_repository.get_by_id(user_id)
         if not user:
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="User does not exist"
                )

      else:
         seller = await self.seller_repository.get_by_user_id(user_id)
         if not seller:
            raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="Seller does not exist"
                )
         

      address = Address(**address_data.model_dump())

      created_address = await self.repository.create(address)

      return AddressRead.model_validate(created_address)


   async def update(self, address_id: UUID, update_data: AddressUpdate) -> AddressRead:
      address = await self.repository.get_address(address_id)
      if not address:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Address not found"
         )

      update_dict = update_data.model_dump(exclude_unset= True)

      for field, value in update_dict.items():
         if hasattr(address, field) and value is not None:
            setattr(address, field, value)

      updated_address = await self.repository.update(address)

      return AddressRead.model_validate(updated_address)


   async def delete(self, address_id: UUID) -> bool:
      result = await self.repository.delete(address_id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Address not found"
         )
      return result

