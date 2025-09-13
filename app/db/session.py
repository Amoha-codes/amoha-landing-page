from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings
from app.db.models import Base
settings= get_settings()

#creating sesssion 
engine = create_async_engine(settings.DB_URL,future=True)
async_session: async_sessionmaker | Any = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

#a async func to get session when needed

async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            print(e)
        finally:
            pass


#initializing db here so models can migrate 
async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

# for get_db.............................................
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from app.db.session import engine  # adjust based on where your engine is defined

# assuming you're using SQLAlchemy async engine
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
# .......................................................

