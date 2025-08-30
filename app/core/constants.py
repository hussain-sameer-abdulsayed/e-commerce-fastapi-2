
## IMAGES CONSTANTS ##
from app import main


UPLOAD_DIRECTORY = "uploads/images"
ALLOWED_MIME_TYPES = ["image/jpeg",  "image/jpg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  ## 5MB
MAX_IMAGES_PER_PRODUCT = 10
ALLOWED_ENTITES = ["product", "category", "user_profile", "seller_profile"]


MAIN_URL = "http://127.0.0.1:8000"