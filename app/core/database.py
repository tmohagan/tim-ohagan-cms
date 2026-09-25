import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# Maps to the host port bound to the cms-postgres container or environment variable
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://cms_user:cms_password@cms-postgres:5432/cms_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
