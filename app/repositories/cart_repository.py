from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.cart_item import CartItem
from sqlalchemy.ext.asyncio import AsyncSession





class CartRepository:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def __update_cart_total(self, cart_id: UUID) -> Cart:
      cart = await self.get_cart_by_id(cart_id)
      if not cart:
         return None
      
      total = sum(item.total for item in cart.cart_items if item.total)
      cart.total = total
      cart.updated_at = datetime.utcnow()

      self.db.add(cart)
      await self.db.commit()
      await self.db.refresh(cart)
      return cart


   async def get_cart_by_id(self, cart_id: UUID) -> Optional[Cart]:
      statement = (
         select(Cart)
         .options(
            selectinload(Cart.cart_items)
            .selectinload(CartItem.product)
            )
         .where(Cart.id == cart_id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()
   

   async def get_cart_by_user_id(self, user_id: UUID) -> Optional[Cart]:
      statement = (
         select(Cart)
         .options(
            selectinload(Cart.cart_items)
            .selectinload(CartItem.product)
            )
         .where(Cart.user_id == user_id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()


   async def get_cart_items_by_cart_id(self, cart_id: UUID) -> List[CartItem]:
      statement = (
         select(CartItem)
         .options(
            selectinload(CartItem.product)
         )
         .where(CartItem.cart_id == cart_id)
      )
      result = await self.db.execute(statement)
      return list(result.scalars().all())


   async def get_cart_total(self, cart_id: UUID) -> Decimal:
      statement = select(Cart.total).where(Cart.id == cart_id)
      result = await self.db.execute(statement)
      total = result.scalar_one_or_none()
      return total if total is not None else Decimal("0.00")


   async def get_cart_item_by_id(self, cart_item_id: UUID) -> Optional[CartItem]:
      statement = (
         select(CartItem)
         .options(selectinload(CartItem.product))
         .where(CartItem.id == cart_item_id)
      )
      result = await self.db.execute(statement)
      return result.scalar_one_or_none()

   async def add_cart_item(self, cart_item: CartItem) -> CartItem:
      self.db.add(cart_item)
      await self.db.commit()
      await self.db.refresh(cart_item)

      await self.__update_cart_total(cart_item.cart_id)
      return cart_item
   

   async def update_cart_item(self, cart_item: CartItem) -> CartItem:
      self.db.add(cart_item)
      await self.db.commit()
      await self.db.refresh(cart_item)

      await self.__update_cart_total(cart_item.cart_id)
      return cart_item


   async def remove_cart_item(self, cart_item_id: UUID) -> bool:
      cart_item = await self.get_cart_item_by_id(cart_item_id)
      if cart_item:
         cart_id = cart_item.cart_id
         await self.db.delete(cart_item)
         await self.db.commit()


         await self.__update_cart_total(cart_id)
         return True
      return False


   async def clear_cart(self, cart_id: UUID) -> bool:
      cart_items = await self.get_cart_items_by_cart_id(cart_id)
      if cart_items:
         for item in cart_items:
            await self.db.delete(item)
         await self.db.commit()
         

         await self.__update_cart_total(cart_id)
         return True
      return False


### This is used when creating user ###
   async def create_cart(self, cart: Cart) -> Cart:
      self.db.add(cart)
      await self.db.commit()
      await self.db.refresh(cart)
      return cart




