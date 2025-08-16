from decimal import Decimal
from typing import List
from uuid import UUID
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.cart_service import CartService
from app.schemas.cart import CartCreate, CartRead, CartWithItems
from app.schemas.cart_item import CartItemCreate, CartItemRead, CartItemUpdate, CartItemWithProduct




router = APIRouter(
   responses={404:{"description":"Not found"}}
)



async def get_cart_service(db: AsyncSession = Depends(get_db)) -> CartService:
   return CartService(db)


@router.get("/{cart_id}", response_model= CartWithItems, status_code= status.HTTP_200_OK)
async def get_cart_by_id(
   cart_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.get_cart_by_id(cart_id= cart_id)
   

@router.get("/users/{user_id}", response_model= CartWithItems, status_code= status.HTTP_200_OK)
async def get_cart_by_user_id(
   user_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.get_cart_by_user_id(user_id= user_id)


@router.get("/items/{cart_id}", response_model= List[CartItemWithProduct], status_code= status.HTTP_200_OK)
async def get_cart_items(
   cart_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.get_cart_items(cart_id= cart_id)


@router.get("/items/item/{item_id}", response_model= CartItemWithProduct, status_code= status.HTTP_200_OK)
async def get_cart_item(
   item_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.get_cart_item(cart_item_id= item_id)


@router.get("/total/{cart_id}", response_model= Decimal, status_code= status.HTTP_200_OK)
async def get_cart_total(
   cart_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.get_cart_total(cart_id= cart_id)


@router.post("/{cart_id}", response_model= CartItemRead, status_code= status.HTTP_201_CREATED)
async def add_item_to_cart(
   cart_id: UUID,
   cart_item_data: CartItemCreate,
   service: CartService = Depends(get_cart_service)
):
   return await service.add_cart_item(cart_id= cart_id, cart_item_data= cart_item_data)


@router.patch("/{item_id}", response_model= CartItemRead, status_code= status.HTTP_200_OK)
async def update_item_quantity(
   item_id: UUID,
   update_data: CartItemUpdate,
   service: CartService = Depends(get_cart_service)
):
   return await service.update_cart_item(cart_item_id= item_id, update_data= update_data)


@router.delete("/items/{item_id}",response_model= bool, status_code= status.HTTP_200_OK)
async def remove_item_from_cart(
   item_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.remove_cart_item(cart_item_id= item_id)


@router.delete("/{cart_id}", response_model= bool, status_code= status.HTTP_200_OK)
async def clear_cart(
   cart_id: UUID,
   service: CartService = Depends(get_cart_service)
):
   return await service.clear_cart(cart_id= cart_id)





