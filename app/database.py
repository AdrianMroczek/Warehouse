from sqlmodel import SQLModel, Field, create_engine, Relationship
from typing import List, Optional

sqlite_file_name = "stocks.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    quantity: int

    category_id: int = Field(foreign_key="category.id")

    category: Optional[Category] = Relationship(back_populates="products")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()