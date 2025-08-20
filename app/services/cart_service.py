from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.repositories.coupon_repository import CouponRepository
from app.schemas.cart import CartCreate, CartRead, CartWithItems
from app.schemas.cart_item import CartItemCreate, CartItemRead, CartItemUpdate, CartItemWithProduct
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository


class CartService:
   def __init__(self, db: AsyncSession):
      self.db = db
      self.repository = CartRepository(db)
      self.product_repository = ProductRepository(db)
      self.coupon_repository = CouponRepository(db)


   async def __validate_cart_item(self, quantity:int, stock_quantity:int):
      
      if stock_quantity == 0:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Out of stock"
         )
      
      if stock_quantity < quantity:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f"only {stock_quantity} available, you request {quantity}"
         )
   

   async def get_cart_by_id(self, cart_id: UUID) -> Optional[CartWithItems]:
      cart = await self.repository.get_cart_by_id(cart_id)
      if not cart:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
         )
      return CartWithItems.model_validate(cart)


   async def get_cart_by_user_id(self, user_id: UUID) -> Optional[CartWithItems]:
      cart = await self.repository.get_cart_by_user_id(user_id)
      if not cart:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
         )
      return CartWithItems.model_validate(cart)


   async def get_cart_items(self, cart_id: UUID) -> List[CartItemWithProduct]:
      cart_items = await self.repository.get_cart_items_by_cart_id(cart_id)
      if not cart_items:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Cart items not found"
         )
      
      return [CartItemWithProduct.model_validate(cart_item) for cart_item in cart_items]


   async def get_cart_total(self, cart_id: UUID) -> Decimal:
      return await self.repository.get_cart_total(cart_id)


   async def get_cart_item(self, cart_item_id: UUID) -> Optional[CartItemWithProduct]:
      cart_item = await self.repository.get_cart_item_by_id(cart_item_id)
      if not cart_item:
         raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Cart item not found"
         )
      return CartItemWithProduct.model_validate(cart_item)


   async def add_cart_item(self, cart_id: UUID, cart_item_data: CartItemCreate) -> CartItemRead:
      cart = await self.repository.get_cart_by_id(cart_id)
      if not cart:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Cart not found"
         )
      
      product = await self.product_repository.get_by_id(cart_item_data.product_id)
      if not product:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
         )
      
      
      existing_cart_item = await self.repository.get_cart_item_by_product(cart_id, cart_item_data.product_id)


      # Product exists - increase quantity
      if existing_cart_item:
         new_quantity = existing_cart_item.quantity + cart_item_data.quantity

         await self.__validate_cart_item(new_quantity, product.stock_quantity)

         existing_cart_item.quantity = new_quantity
         existing_cart_item.total
         existing_cart_item.updated_at = datetime.utcnow()

         updated_cart_item = await self.repository.update_cart_item(existing_cart_item)

         return CartItemRead.model_validate(updated_cart_item)
      

      # Product doesn't exist - create new cart item
      else:
         await self.__validate_cart_item(cart_item_data.quantity, product.stock_quantity)
      
      cart_item = CartItem(
         cart_id= cart_id,
         product_id = product.id,
         quantity= cart_item_data.quantity,
         unit_price= product.price
      )

      created_cart_item = await self.repository.add_cart_item(cart_item)

      return CartItemRead.model_validate(created_cart_item)


   async def update_cart_item(self, cart_item_id: UUID, update_data: CartItemUpdate) -> CartItemRead:
      cart_item = await self.repository.get_cart_item_by_id(cart_item_id)
      if not cart_item:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Cart item not found"
         )
      
      product = await self.product_repository.get_by_id(cart_item.product_id)
      if not product:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
         )
      
      await self.__validate_cart_item(update_data.quantity, product.stock_quantity)
      
      cart_item.quantity = update_data.quantity
      cart_item.updated_at = datetime.utcnow()

      updated_cart_item = await self.repository.update_cart_item(cart_item)
      return CartItemRead.model_validate(updated_cart_item)
      
      
   async def remove_cart_item(self, cart_item_id: UUID) -> bool:
      result = await self.repository.remove_cart_item(cart_item_id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Cart item not found"
         )
      return result


   async def clear_cart(self, cart_id: UUID) -> bool:
      result = await self.repository.clear_cart(cart_id)
      if not result:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Cart not found"
         )
      return result


   async def apply_coupon_to_cart(self, cart_id: UUID, coupon_code: UUID) -> CartRead:
      coupon = await self.coupon_repository.get_by_code(coupon_code)
      if not coupon or coupon.is_currently_active == False:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Coupon does not exists or expired"
         )
      
      cart = await self.repository.get_cart_by_id(cart_id)
      if not cart or not cart.cart_items:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Cart not found or crt is empty"
         )
      
      if cart.total and cart.total < coupon.min_order_amount:
         raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f"The minimum total amout is {coupon.min_order_amount}, your total is {cart.total}"
         )

      cart.updated_at = datetime.utcnow()
      updated_cart = await self.repository.apply_coupon_to_cart(coupon, cart)
      return CartRead.model_validate(updated_cart)





