from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.database import engine, Category, Product, create_db_and_tables

app = FastAPI(title="Product Catalog API")

# Open and close session for each request
def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
# Create database and tables on startup if they don't exist
def on_startup():
    create_db_and_tables()

@app.post("api/seed", tags=["Administrator"])
    def seed_database(session: Session = Depends(get_session)):
    """Adds initial data to the database."""
    if session.exec(select(Category)).first():
        return {"message": "Databese empty."}