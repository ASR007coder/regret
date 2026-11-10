# backend/database/connection.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------
# 1. BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# 2. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# 3. DATABASE URL
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(BASE_DIR / 'regret.db').as_posix()}"
)

# --------------------------------------------------
# 4. DATABASE ENGINE
# --------------------------------------------------

engine = create_engine(
    url=DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# --------------------------------------------------
# 5. SESSION FACTORY
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# --------------------------------------------------
# 6. DATABASE DEPENDENCY
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()