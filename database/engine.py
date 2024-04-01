from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import DB_LITE
from database.models import Base

engine = create_async_engine(DB_LITE, echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)