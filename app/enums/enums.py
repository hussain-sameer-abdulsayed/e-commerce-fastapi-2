from enum import Enum
import sqlalchemy as sa

class Province(str, Enum):
    BAGHDAD = "baghdad"
    BASRAH = "basrah"
    NINAWA = "ninawa"
    ERBIL = "erbil"
    KIRKUK = "kirkuk"
    SULAYMANIYAH = "sulaymaniyah"
    DUHOK = "duhok"
    ANBAR = "anbar"
    BABIL = "babil"
    NAJAF = "najaf"
    KARBALA = "karbala"
    MAYSAN = "maysan"
    DIYALA = "diyala"
    WASIT = "wasit"
    SALAHADDIN = "salahaddin"
    MUTHANNA = "muthanna"
    THIQAR = "thiqar"

    # Add this method to help SQLAlchemy handle the enum properly
    def __str__(self):
        return self.value

class Order_Status(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def __str__(self):
        return self.value

class Discount_Model_Type(str, Enum):
    CATEGORY = "category"
    PRODUCT = "product"
    SHIPMENT = "shipment"

    def __str__(self):
        return self.value

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

    def __str__(self):
        return self.value