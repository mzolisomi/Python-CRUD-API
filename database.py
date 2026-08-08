import os

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv 

load_dotenv()

DB_USER: str | None = os.getenv("DB_User")
DB_PASSWORD: str | None = os.getenv("DB_Password")
DB_HOST: str | None = os.getenv("DB_Host")
DB_PORT: str | None = os.getenv("DB_Port")
DB_NAME: str | None = os.getenv("DB_Name")

conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

engine = create_engine(conn_string)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()