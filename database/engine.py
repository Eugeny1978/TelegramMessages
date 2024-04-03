from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import DB_LITE, DB_PostgreSQL
from database.models import Base

# Движок для SQLite DB
# engine = create_async_engine(DB_LITE, echo=True)
engine = create_async_engine(DB_PostgreSQL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)