from fastapi import Depends
from typing import Annotated, Generator
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base


from time import sleep

from src.models.schema_models import Base, User, Group

# Database credentials
DATABASE_URL = "postgresql://postgres:mysecretpassword@postgres_db:5432/splitwise_db"

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Test the connection
no_of_retries = 12
sleep_interval_seconds = 5

while no_of_retries >= 0:
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connected to the database:", result.fetchone())
            break
    except Exception as e:
        print("Error connecting to the database:", e)
        no_of_retries -= 1
        sleep(3)
        
    
    
def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
def create_schema():
    Base.metadata.create_all(engine)
    
def add_seed_data():
    users = [
        User(user_name="bhargav", password="sjdbvskbvs"),
        User(user_name="kunj", password="sjdbvskbvs"),
        User(user_name="dhruv", password="sdvsvsdvs"),
        User(user_name="krunal", password="dvsavasvd"),
        User(user_name="meet", password="kefnskdjv")
    ]
    
    
    with Session(engine) as session:
        user_query = select(User)
        users_list = [user for user in session.scalars(user_query)]
        
        if len(users_list) >= 5:
            return
        
        session.add_all(users)
        session.commit()
    
    
SessionDep = Annotated[Session, Depends(get_db_session)]
    