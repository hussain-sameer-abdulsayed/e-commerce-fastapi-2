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


# Exported schemas for easy importing
__all__ = [
    # Base
    "BaseSchemaConfig",
    
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserRead",
    "UserProfileBase", "UserProfileCreate", "UserProfileUpdate", "UserProfileRead",
    
    # Seller
    "SellerProfileBase", "SellerProfileCreate", "SellerProfileUpdate", "SellerProfileRead",
    
    # Address
    "AddressBase", "AddressCreate", "AddressUpdate", "AddressRead",
    
    # Category
    "CategoryBase", "CategoryCreate", "CategoryUpdate", "CategoryRead", "CategoryWithProducts", "CategoryDiscountBase", "CategoryDiscountCreate", "CategoryDiscountUpdate", "CategoryDiscountRead",
    
    # Product
    "ProductBase", "ProductCreate", "ProductUpdate", "ProductRead",
    "ProductDiscountBase", "ProductDiscountCreate", "ProductDiscountUpdate", "ProductDiscountRead",
    "ProductReviewBase", "ProductReviewCreate", "ProductReviewUpdate", "ProductReviewRead",
    
    # Cart
    "CartBase", "CartCreate", "CartRead", "CartWithItems",
    "CartItemBase", "CartItemCreate", "CartItemUpdate", "CartItemRead",
    
    # Order
    "OrderBase", "OrderCreate", "OrderUpdate", "OrderRead", "OrderWithItems",
    "OrderItemBase", "OrderItemCreate", "OrderItemUpdate", "OrderItemRead",
    
    # Coupon
    "CouponBase", "CouponCreate", "CouponUpdate", "CouponRead",
    "CouponUsageBase", "CouponUsageCreate", "CouponUsageRead",
    "CouponSetStatus"
    
    # Shipment
    "ShipmentBase", "ShipmentCreate", "ShipmentUpdate", "ShipmentRead",
    "ShipmentDiscountBase", "ShipmentDiscountCreate", "ShipmentDiscountUpdate", "ShipmentDiscountRead",
]