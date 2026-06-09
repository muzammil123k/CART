import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
URL_DATABASE = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if URL_DATABASE.startswith("sqlite"):
    engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})
else:
    engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()