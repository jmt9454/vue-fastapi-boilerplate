from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()

# 2. Get the Database URL
# Default to SQLite if not found in .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

# 3. Create the Engine
# Note: SQLite needs "check_same_thread": False. Postgres does not.
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)

# 4. Create the SessionLocal
# This is what we use to actually talk to the DB in a request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base
# All models (Student, User, etc.) will inherit from this
Base = declarative_base()