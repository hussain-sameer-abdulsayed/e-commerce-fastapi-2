from sqlmodel import Field, SQLModel
from uuid import UUID

class ProductCategoryLink(SQLModel, table=True):
    __tablename__ = "product_categories"  # type: ignore
    
    product_id: UUID = Field(foreign_key="products.id", primary_key=True, index=True)
    category_id: UUID = Field(foreign_key="categories.id", primary_key=True, index=True)