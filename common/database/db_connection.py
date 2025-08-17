from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from common.config import settings

# SQLite connection string
DATABASE_URL = f"sqlite:///{settings.sqlite_path}"

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False},  # needed for SQLite + threads
    # future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
