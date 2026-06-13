import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Default to MySQL but allow override via environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1531@localhost/dsa_tracker")

# Handle SQLite carefully (check for sqlite prefix and set check_same_thread)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()