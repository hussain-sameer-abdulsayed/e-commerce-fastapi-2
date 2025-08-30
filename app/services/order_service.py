
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select
from uuid import UUID
from typing import List, Optional

from app.enums.enums import Order_Status
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderRead, OrderCreate, OrderWithItems, OrderUpdate
from app.schemas.order_item import OrderItemCreate, OrderItemRead, OrderItemUpdate

class OrderService:
   def __init__(self, db: AsyncSession) -> None:
      self.db = db
      self.repository = OrderRepository(db)


   async def get_all(self) -> List[OrderRead]:
      orders = await self.repository.get_all()
      return [OrderRead.model_validate(order) for order in orders]
   

   async def get_by_id(self, order_id: UUID) -> OrderRead:
      order = await self.repository.get_by_id(order_id)
      if not order:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="order Not found"
         )
      return OrderRead.model_validate(order)


   async def get_by_order_number(self, order_number: UUID) -> OrderRead:
      order = await self.repository.get_by_order_number(order_number)
      if not order:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="order Not found"
         )
      return OrderRead.model_validate(order)


   async def get_by_status(self, order_status: Order_Status) -> OrderRead:
      order = await self.repository.get_by_status(order_status)
      if not order:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="order Not found"
         )
      return OrderRead.model_validate(order)


   async def create(self, order_data: OrderCreate):
      pass


   async def update(self, order_id: UUID, update_data: OrderUpdate):
      order = await self.repository.get_by_id(order_id)
      if not order:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Order not found"
         )
      
      data_dict = update_data.model_dump(exclude_unset= True)

      for field, value in data_dict.items():
         if hasattr(order, field) and value is not None:
            setattr(order, field, value)

      updated_order = await self.repository.update(order)

      return OrderRead.model_validate(updated_order)


   async def delete(self, order_id: UUID) -> bool:
      success = await self.repository.delete(order_id)
      if not success:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Order not found"
         )
      return success
   

   async def update_status(self, order_id: UUID, order_status: Order_Status) -> OrderRead:
      order = await self.repository.update_status(order_id, order_status)
      if not order:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Order not found"
         )
      return OrderRead.model_validate(order)


