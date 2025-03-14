from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import pool
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
