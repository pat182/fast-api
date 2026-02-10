import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings

Base = declarative_base()

def get_sync_database_url():
    # CI/test mode: use SQLite in memory
    if settings.DB_HOST == "sqlite":
        return "sqlite:///:memory:"

    # Production/dev: build MySQL URL safely
    password = urllib.parse.quote_plus(str(settings.DB_PASSWORD or ""))
    return (
        f"mysql+pymysql://{settings.DB_USER}:{password}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

def get_async_database_url():
    # CI/test mode: use SQLite in memory
    if settings.DB_HOST == "sqlite":
        return "sqlite+aiosqlite:///:memory:"

    # Production/dev: build MySQL URL safely
    password = urllib.parse.quote_plus(str(settings.DB_PASSWORD or ""))
    return (
        f"mysql+aiomysql://{settings.DB_USER}:{password}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

# -------------------------
# Sync setup (pymysql)
# -------------------------
SYNC_DATABASE_URL = get_sync_database_url()
engine = create_engine(SYNC_DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Async setup (aiomysql)
# -------------------------
ASYNC_DATABASE_URL = get_async_database_url()
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=settings.DEBUG, future=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session