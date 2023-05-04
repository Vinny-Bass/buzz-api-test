from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://buzz:buzz@localhost:5555/buzz_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db_session():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
