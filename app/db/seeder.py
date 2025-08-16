import asyncio
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .database import engine, AsyncSessionLocal
from app.models import User, UserProfile, SellerProfile, Category, Product, ProductCategoryLink, Coupon, Shipment, Cart
from app.enums.enums import Province, Gender


class DatabaseSeeder:
   def __init__(self, db: AsyncSession):
      self.db = db


   async def get_existing_users(self) -> list[User]:
      """Get existing users from database"""
      result = await self.db.execute(select(User).order_by(User.created_at))
      return list(result.scalars().all())


   async def seed_users(self) -> list[User]:
      print("________Seeding users________")

      # Check if users already exist
      existing_users = await self.get_existing_users()
      if existing_users:
         print("👥 Users already exist, returning existing users...")
         return existing_users  # Return existing users instead of None
      

      users_data = [
         {
            "user_name": "admin_user",
            "full_name": "Admin User",
            "phone_number": "1234567890",
            "email": "admin@fastapi.com",
            "password_hash": "hashed_password_123"
         },
         {
            "user_name": "hussain_123",
            "full_name": "Hussain",
            "phone_number": "07849678401",
            "email": "lifereal3310@gmail.com",
            "password_hash": "hashed_password_123"
         }
      ]

      created_users = []
      for user_data in users_data:
         user = User(**user_data)
         self.db.add(user)
         created_users.append(user)

      await self.db.commit()

      for user in created_users:
         await self.db.refresh(user)

      print(f"✅ Created {len(created_users)} users")
      return created_users
   
   
   async def seed_carts(self, users: list[User]) -> list[Cart]:
      if not users or len(users) < 2:
         print("⚠️ Not enough users to create carts, skipping...")
         return None
      
      carts_data = [
         {
            "user_id": users[0].id
         },
         {
            "user_id": users[1].id
         }
      ]

      created_carts = []
      for cart_data in carts_data:
         cart = Cart(**cart_data)
         self.db.add(cart)
         created_carts.append(cart)
      
      await self.db.commit()
      print(f"✅ Created {len(created_carts)} carts")
      return created_carts


   async def seed_user_profiles(self, users: list[User]) -> UserProfile:
      if not users or len(users) < 2:
            print("⚠️ Not enough users to create profiles, skipping...")
            return None
        
        # Check if profiles already exist
      result = await self.db.execute(select(UserProfile))
      exists_profile = result.scalar_one_or_none()
      if exists_profile:
         print("👤 User profiles already exist, skipping...")
         return exists_profile

      profiles_data = [
         {
            "user_id": users[0].id,
            "bio": "Admin user created with seeding",
            "main_image_url": "https://example.com/john.jpg",
            "gender": Gender.MALE,
            "birth_date": datetime(1990, 1, 1)
         },
         {
            "user_id": users[1].id,
            "bio": "Backend developer created with seeding",
            "main_image_url": "https://example.com/john.jpg",
            "gender": Gender.MALE,
            "birth_date": datetime(2003, 8, 3)
         }
      ]

      created_profiles = []
      for profile_data in profiles_data:
         profile = UserProfile(**profile_data)
         self.db.add(profile)
         created_profiles.append(profile)


      await self.db.commit()

      for created_profile in created_profiles:
         await self.db.refresh(created_profile)

      print(f"✅ Craeted {len(created_profiles)} user profiles")
      return created_profiles


   async def seed_seller_profiles(self, users: list[User]) -> SellerProfile:
      print("______Seeding seller profiles______")

      if not users or len(users) < 2:
            print("⚠️ Not enough users to create seller profile, skipping...")
            return None
        
        # Check if seller profile already exists
      result = await self.db.execute(select(SellerProfile))
      existing_seller = result.scalar_one_or_none()
      if existing_seller:
         print("🏪 Seller profile already exists, returning existing...")
         return existing_seller

      profile_data = {
            "user_id": users[0].id,
            "store_name": "Point Mobile",
            "main_image_url": "https://example.com/john.jpg",
            "store_description": "Point Mobile Point Mobile Point Mobile",
            "store_phone_number": "123456780"
         }
      

      profile = SellerProfile(**profile_data)
      self.db.add(profile)
      await self.db.commit()
      await self.db.refresh(profile)

      print(f"✅ Craeted user profiles")
      return profile


   async def seed_categories(self, admin_user: User) -> list[Category]:
      print("______Seeding categories______")

      if not admin_user:
         print("⚠️ No admin user available, skipping categories...")
         return []
      
      # Check if categories already exist
      result = await self.db.execute(select(Category))
      existing_categories = list(result.scalars().all())
      if existing_categories:
         print("📂 Categories already exist, returning existing...")
         return existing_categories


      categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and gadgets",
                "main_image_url": "https://example.com/electronics.jpg",
                "created_by_id": admin_user.id
            },
            {
                "name": "Books",
                "description": "Books and educational materials",
                "main_image_url": "https://example.com/books.jpg",
                "created_by_id": admin_user.id
            },
            {
                "name": "Home & Garden",
                "description": "Home improvement and garden supplies",
                "main_image_url": "https://example.com/home.jpg",
                "created_by_id": admin_user.id
            },
            {
                "name": "Clothing",
                "description": "Fashion and apparel",
                "main_image_url": "https://example.com/clothing.jpg",
                "created_by_id": admin_user.id
            },
            {
                "name": "Sports",
                "description": "Sports equipment and fitness gear",
                "main_image_url": "https://example.com/sports.jpg",
                "created_by_id": admin_user.id
            }
        ]
      
      created_categories = []
      for category_data in categories_data:
         category = Category(**category_data)
         self.db.add(category)
         created_categories.append(category)

      await self.db.commit()
      
      for category in created_categories:
         await self.db.refresh(category)

      print(f"✅ Created {len(created_categories)} categories")
      return created_categories
   

   async def seed_products(self, categories: list[Category], seller_profile: SellerProfile) -> list[Product]:
      print("______Seeding products______")

      if not categories or not seller_profile:
         print("⚠️ Missing categories or seller profile, skipping products...")
         return []
      
      result = await self.db.execute(select(Product))
      existing_products = list(result.scalars().all())
      if existing_products:
         print("📦 Products already exist, returning existing...")
         return existing_products
      

   
      products_data = [
            {
                "name": "iPhone 15 Pro",
                "price": Decimal("999.99"),
                "stock_quantity": 50,
                "description": "Latest iPhone with advanced camera system",
                "main_image_url": "https://example.com/iphone15.jpg",
                "seller_profile_id": seller_profile.id
            },
            {
                "name": "Samsung Galaxy S24",
                "price": Decimal("899.99"),
                "stock_quantity": 30,
                "description": "Flagship Android smartphone",
                "main_image_url": "https://example.com/galaxy-s24.jpg",
                "seller_profile_id": seller_profile.id
            },
            {
                "name": "MacBook Air M3",
                "price": Decimal("1299.99"),
                "stock_quantity": 25,
                "description": "Ultra-thin laptop with M3 chip",
                "main_image_url": "https://example.com/macbook.jpg",
                "seller_profile_id": seller_profile.id
            },
            {
                "name": "Nike Air Max",
                "price": Decimal("129.99"),
                "stock_quantity": 100,
                "description": "Comfortable running shoes",
                "main_image_url": "https://example.com/nike.jpg",
                "seller_profile_id": seller_profile.id
            },
            {
                "name": "Programming Book Bundle",
                "price": Decimal("49.99"),
                "stock_quantity": 200,
                "description": "Collection of programming books",
                "main_image_url": "https://example.com/books.jpg",
                "seller_profile_id": seller_profile.id
            }
        ]

      created_products = []
      for product_data in products_data:
         product = Product(**product_data)
         self.db.add(product)
         created_products.append(product)

      await self.db.commit()

      for product in created_products:
         await self.db.refresh(product)

      # Create product-category relationships
      product_category_links = [
         (created_products[0], categories[0]),
         (created_products[1], categories[0]),
         (created_products[2], categories[0]),
         (created_products[3], categories[3]),
         (created_products[3], categories[4]),
         (created_products[4], categories[1])
      ]

      for product, category in product_category_links:
         link = ProductCategoryLink(product_id= product.id, category_id= category.id)
         self.db.add(link)
      
      await self.db.commit()

      print(f"✅ Created {len(created_products)} products with category links")
      return created_products
   

   async def seed_shipments(self):
      print("______Seeding shipments______")

      # Check if shipments already exist
      result = await self.db.execute(select(Shipment))
      existing_shipments = list(result.scalars().all())
      if existing_shipments:
         print("🚚 Shipments already exist, skipping...")
         return existing_shipments

      Shipments_data = [
         {
            "province": Province.BAGHDAD,
            "cost": Decimal("5000.00")
         },
         {
            "province": Province.NAJAF,
            "cost": Decimal("8000.00")
         },
         {
            "province": Province.KARBALA,
            "cost": Decimal("7000.00")
         },
         {
            "province": Province.BABIL,
            "cost": Decimal("6000.00")
         },
         {
            "province": Province.BASRAH,
            "cost": Decimal("10000.00")
         }
      ]
   
      created_shipments = []
      for shipment_data in Shipments_data:
         shipment = Shipment(**shipment_data)
         self.db.add(shipment)
         created_shipments.append(shipment)
      
      await self.db.commit()
      print(f"✅ Created {len(created_shipments)} shipment options")
      return created_shipments

   
   async def seed_coupons(self):
      print("______Seeding coupons______")

      # Check if coupons already exist
      result = await self.db.execute(select(Coupon))
      if result.first():
         print("🎫 Coupons already exist, skipping...")
         return


      coupons_data = [
         {
            "code": "WELCOME50",
            "discount_amount": 50,
            "min_order_amount": Decimal("50000.00"),
            "max_uses": 100,
            "start_at": datetime.utcnow(),
            "end_at": datetime(2025, 10, 10),
            "is_active": True
         },
         {
            "code": "SAVE20",
            "discount_amount": 10,
            "min_order_amount": Decimal("100000.00"),
            "max_uses": 50,
            "start_at": datetime.utcnow(),
            "end_at": datetime(2026, 8, 7),
            "is_active": True
         }
      ]

      for coupon_data in coupons_data:
         coupon = Coupon(**coupon_data)
         self.db.add(coupon)
      
      await self.db.commit()
      print(f"✅ Created {len(coupons_data)} coupons")


   async def seed_all(self):
      print("______Starting database seeding______")

      try:
         users = await self.seed_users()
         await self.seed_carts(users)
         await self.seed_user_profiles(users)
         seller_profile = await self.seed_seller_profiles(users)
         categories = await self.seed_categories(users[0] if users else None)
         await self.seed_products(categories, seller_profile)
         await self.seed_shipments()
         await self.seed_coupons()

         print("🎉 Database seeding completed successfully!")
      

      except Exception as e:
         print(f"❌ Error during seeding: {e}")
         await self.db.rollback()
         raise




async def seed_database():
   """ main seeding function """
   async with AsyncSessionLocal() as db:
      seeder = DatabaseSeeder(db)
      await seeder.seed_all()



