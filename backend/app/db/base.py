"""SQLAlchemy ORM base and database session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from ..config import get_settings

settings = get_settings()

# Sync engine and session for synchronous operations
engine = create_engine(settings.database_url, echo=settings.debug, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session for async operations
async_engine = create_async_engine(settings.database_async_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Base class for all models
Base = declarative_base()


def get_db() -> Session:
    """Dependency to get database session for sync endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        yield session
