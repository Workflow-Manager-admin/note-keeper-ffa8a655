import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Fetch database configuration from environment variables
DB_URL = os.getenv("NOTE_APP_DB_URL")
if not DB_URL:
    raise ValueError("NOTE_APP_DB_URL environment variable not set. Please add it to your .env file.")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# PUBLIC_INTERFACE
def get_db():
    """FastAPI dependency that provides a SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
