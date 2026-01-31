from fastapi import FastAPI, Depends, HTTPException, Request
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from app.database import engine, Category, Product, create_db_and_tables, CategoryRead, ProductRead
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category_name: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database and tables on startup."""
    create_db_and_tables()
    yield

app = FastAPI(
    title="Warehouse Management API",
    lifespan=lifespan,
    servers=[{"url": "http://127.0.0.1:8000/", "description": "Local server"}]
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

def get_session():
    """Open and close session for each request"""
    with Session(engine) as session:
        yield session

# --- Admin Endpoints ---

@app.post("/api/seed", tags=["Admin"])
def seed_database(session: Session = Depends(get_session)):
    """Adds exemplary data to the database."""
    if session.exec(select(Category)).first():
        return {"message": "Databese not empty. Seeding skipped"}

    cat_monitors = Category(name="Monitory")
    cat_laptopy = Category(name="Laptopy")
    cat_myszy = Category(name="Myszy")
    session.add_all([cat_monitors, cat_laptopy, cat_myszy])
    session.commit()

    session.refresh(cat_monitors)
    session.refresh(cat_laptopy)
    session.refresh(cat_myszy)

    p1 = Product(name="Lenovo Legion 27Q-10", price=799.99, quantity=20, category_id=cat_monitors.id)
    p2 = Product(name="Samsung Odyssey G5", price=1799.99, quantity=15, category_id=cat_monitors.id)
    p3 = Product(name="Logitech Lift", price=249.99, quantity=150, category_id=cat_myszy.id)
    p4 = Product(name="ASUS ROG Strix G16", price=4999.99, quantity=7, category_id=cat_laptopy.id)
    session.add_all([p1, p2, p3, p4])
    session.commit()

    return {"message": "Database seeding successful"}

# --- Client Endpoints ---

@app.post("/api/products/{product_id}/order", tags=["Client"])
def order_product(product_id: int, order_quantity: int, session: Session = Depends(get_session)):
    """Order a product by its ID."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")
    if order_quantity > product.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")

    product.quantity -= order_quantity
    session.add(product)
    session.commit()
    session.refresh(product)
    return {"message": f"Ordered {product.name}", "remaining": product.quantity}

# --- Employee Endpoints ---

@app.post("/api/employee/products", tags=["Employee"])
def add_product(product_in: ProductCreate, session: Session = Depends(get_session)):
    """Add new product to the catalog."""
    statement = select(Category).where(Category.name == product_in.category_name)
    category = session.exec(statement).first()
    if not category:
        category = Category(name=product_in.category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    statement_prod = select(Product).where(Product.name == product_in.name)
    existing_product = session.exec(statement_prod).first()

    if existing_product:
        existing_product.quantity += product_in.quantity
        existing_product.price = product_in.price
        session.add(existing_product)
        db_product = existing_product
    else:

        db_product = Product(
        name=product_in.name,
        price=product_in.price,
        quantity=product_in.quantity,
        category_id=category.id
    )

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product

@app.post("/api/employee/categories", tags=["Employee"])
def add_category(category_in: Category, session: Session = Depends(get_session)):
    """Add new category to the catalog."""
    session.add(category_in)
    session.commit()
    session.refresh(category_in)
    return category_in


@app.get("/api/products", response_model=List[ProductRead], tags=["Employee"])
def get_products(
        session: Session = Depends(get_session),
        category_id: int = None,
        name: str = None,
        max_price: float = None,
        status: str = None
):
    statement = select(Product)

    # Category filter
    if category_id:
        statement = statement.where(Product.category_id == category_id)

    # Name filter
    if name:
        statement = statement.where(Product.name.contains(name))

    # Price filter
    if max_price:
        statement = statement.where(Product.price <= max_price)

    # Availability filter
    if status == "in_stock":
        statement = statement.where(Product.quantity > 0)
    elif status == "out_of_stock":
        statement = statement.where(Product.quantity <= 0)

    return session.exec(statement).all()

@app.get("/api/categories", response_model=List[CategoryRead], tags=["Employee"])
def get_categories(session: Session = Depends(get_session)):
    """Retrieve all categories from db."""
    return session.exec(select(Category)).all()

#--- HTML Endpoints ---
@app.get("/", response_class=HTMLResponse, tags=["UI"])
def read_root(request: Request, session: Session = Depends(get_session)):
    """Render the main page with product listings."""
    products = session.exec(select(Product)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products}
    )