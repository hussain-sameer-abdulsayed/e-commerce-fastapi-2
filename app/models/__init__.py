# app/models/__init__.py - Alternative approach for complex imports
"""
SQLModel database models with careful import order
"""

# Import independent models first
from .user import User, UserBase
from .category import Category, CategoryBase

# Import link tables early
from .product_category import ProductCategoryLink

# Import models that depend on base models
from .user_profile import UserProfile, UserProfileBase
from .seller_profile import SellerProfile, SellerProfileBase
from .address import Address, AddressBase

# Import models with relationships
from .product import Product, ProductBase
from .coupon import Coupon, CouponBase
from .shipment import Shipment, ShipmentBase

# Import models that depend on many others
from .cart import Cart, CartBase
from .cart_item import CartItem, CartItemBase
from .product_review import ProductReview, ProductReviewBase
from .coupon_usage import CouponUsage, CouponUsageBase

# Import discount models
from .product_discount import ProductDiscount
from .category_discount import CategoryDiscount
from .shipment_discount import ShipmentDiscount

# Import complex models last
from .order import Order, OrderBase
from .order_item import OrderItem, OrderItemBase

__all__ = [
    "User", "UserBase", "UserProfile", "UserProfileBase",
    "SellerProfile", "SellerProfileBase", "Address", "AddressBase",
    "Category", "CategoryBase", "Product", "ProductBase", "ProductCategoryLink",
    "ProductReview", "ProductReviewBase", "ProductDiscount",
    "CategoryDiscount", "Cart", "CartBase",
    "CartItem", "CartItemBase", "Coupon", "CouponBase",
    "CouponUsage", "CouponUsageBase", "Shipment", "ShipmentBase",
    "ShipmentDiscount", "Order", "OrderBase",
    "OrderItem", "OrderItemBase",
]