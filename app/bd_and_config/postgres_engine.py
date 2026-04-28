from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.bd_and_config.config1 import setbase
from collections.abc import AsyncGenerator

DATABASEPG_URL = setbase.DATABASEPG_URL

engine = create_async_engine(url=DATABASEPG_URL)

async_session_pg = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base_Pg(DeclarativeBase): 
    pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_pg() as session:
        yield session