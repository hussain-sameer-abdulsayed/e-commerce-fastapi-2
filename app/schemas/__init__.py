from .address import AddressCreate, AddressRead, AddressUpdate
from .cart_item import CartItemCreate, CartItemRead, CartItemUpdate
from .cart import CartCreate, CartRead, CartWithItems
from .category_discount import CategoryDiscountCreate, CategoryDiscountUpdate, CategoryDiscountRead
from .category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryWithProducts
from .coupon_usage import CouponUsageCreate, CouponUsageRead
from .coupon import CouponCreate, CouponRead, CouponUpdate, CouponSetStatus
from .order_item import OrderItemCreate, OrderItemRead, OrderItemUpdate
from .order import OrderCreate, OrderRead, OrderUpdate, OrderWithItems
from .product_discount import ProductDiscountCreate, ProductDiscountRead, ProductDiscountUpdate
from .product_review import ProductReviewCreate, ProductReviewRead, ProductReviewUpdate
from .product import ProductCreate, ProductRead, ProductUpdate
from .seller_profile import SellerProfileCreate, SellerProfileRead, SellerProfileUpdate
from .shipment_discount import ShipmentDiscountCreate, ShipmentDiscountRead, ShipmentDiscountUpdate
from .shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .user_profile import UserProfileCreate, UserProfileRead, UserProfileUpdate
from .user import UserCreate, UserRead, UserUpdate
from .image import ImageCreate, ImageRead, ImageUpdate
from .base_schema import BaseSchemaConfig, BaseSchema

# Exported schemas for easy importing
__all__ = [
    # Base
    "BaseSchemaConfig", "BaseSchema"
    # User
    "UserCreate", "UserUpdate", "UserRead",
    , "UserProfileCreate", "UserProfileUpdate", "UserProfileRead", # type: ignore
    
    # Seller
    "SellerProfileBase", "SellerProfileCreate", "SellerProfileUpdate", "SellerProfileRead",
    
    # Address
    "AddressCreate", "AddressUpdate", "AddressRead",
    
    # Category
    "CategoryCreate", "CategoryUpdate", "CategoryRead", "CategoryWithProducts", "CategoryDiscountCreate", "CategoryDiscountUpdate", "CategoryDiscountRead",
    
    # Product
    "ProductCreate", "ProductUpdate", "ProductRead",
    "ProductDiscountCreate", "ProductDiscountUpdate", "ProductDiscountRead",
    "ProductReviewCreate", "ProductReviewUpdate", "ProductReviewRead",
    
    # Cart
    "CartCreate", "CartRead", "CartWithItems",
    "CartItemCreate", "CartItemUpdate", "CartItemRead",
    
    # Order
    "OrderCreate", "OrderUpdate", "OrderRead", "OrderWithItems",
    "OrderItemCreate", "OrderItemUpdate", "OrderItemRead",
    
    # Coupon
    "CouponCreate", "CouponUpdate", "CouponRead",
    "CouponUsageCreate", "CouponUsageRead",
    "CouponSetStatus"
    
    # Shipment
    "ShipmentCreate", "ShipmentUpdate", "ShipmentRead",
    "ShipmentDiscountCreate", "ShipmentDiscountUpdate", "ShipmentDiscountRead",

    # Image
    "ImageCreate", "ImageRead", "ImageUpdate"
]