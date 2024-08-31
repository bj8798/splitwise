from fastapi import Depends
from typing import Annotated, Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from src.models.schema_models import Base

# Database credentials
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:6432/splitwise_db"

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connected to the database:", result.fetchone())
except Exception as e:
    print("Error connecting to the database:", e)
    
    
def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
def create_schema():
    Base.metadata.create_all(engine)
    print("Schema Created.")
    
SessionDep = Annotated[Session, Depends(get_db_session)]
    