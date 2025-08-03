def initialize_models():
    """
    Initialize all models in the correct order to avoid circular import issues
    """
    # Import all models first
    from app.models.user import User
    from app.models.user_profile import UserProfile
    from app.models.seller_profile import SellerProfile
    from app.models.address import Address
    from app.models.category import Category
    from app.models.product import Product
    from app.models.product_category import ProductCategoryLink
    from app.models.product_review import ProductReview
    from app.models.product_discount import ProductDiscount
    from app.models.cart import Cart
    from app.models.cart_item import CartItem
    from app.models.coupon import Coupon
    from app.models.coupon_usage import CouponUsage
    from app.models.order import Order
    from app.models.order_item import OrderItem
    from app.models.shipment import Shipment
    from app.models.shipment_discount import ShipmentDiscount
    from app.models.category_discount import CategoryDiscount
    
    # Rebuild models in dependency order
    models_to_rebuild = [
        User,
        UserProfile,
        SellerProfile,
        Address,
        Category,
        Product,
        ProductCategoryLink,
        ProductReview,
        ProductDiscount,
        Cart,
        CartItem,
        Coupon,
        CouponUsage,
        Order,
        OrderItem,
        Shipment,
        ShipmentDiscount,
        CategoryDiscount,
    ]
    
    for model in models_to_rebuild:
        try:
            model.model_rebuild()
        except Exception as e:
            print(f"Warning: Could not rebuild {model.__name__}: {e}")
    
    return {
        'User': User,
        'UserProfile': UserProfile,
        'SellerProfile': SellerProfile,
        'Address': Address,
        'Category': Category,
        'Product': Product,
        'ProductCategoryLink': ProductCategoryLink,
        'ProductReview': ProductReview,
        'ProductDiscount': ProductDiscount,
        'Cart': Cart,
        'CartItem': CartItem,
        'Coupon': Coupon,
        'CouponUsage': CouponUsage,
        'Order': Order,
        'OrderItem': OrderItem,
        'Shipment': Shipment,
        'ShipmentDiscount': ShipmentDiscount,
        'CategoryDiscount': CategoryDiscount,
    }