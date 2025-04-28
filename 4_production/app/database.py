# Establish a connection to the PostgreSQL database using SQLAlchemy
# Configures database session
# Is imported into crud.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve database credentials from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Create the database URL using the environment variables
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}" 
#db instead of localhost, since fastapi and db as services are in the same docker network

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL) # This is the connection to the database

# Create a SessionLocal class for each database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Base class for SQLAlchemy models
Base = declarative_base()

# Create tables (optional)
def init_db():
    # Create all tables that are defined in Base metadata
    Base.metadata.create_all(bind=engine)
