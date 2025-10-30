import settings
from loguru import logger
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


session = "placeholder"

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=False,
)


AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db_session():

    async with AsyncSessionLocal() as session:

        logger.info("DB session created")

        try:
            yield session
        except Exception as e:

            logger.error(f"Error during DB session: {e}")

            await session.rollback()
            raise e
        finally:

            logger.info("Closing DB session")

            await session.close()


@asynccontextmanager
async def get_session():

    async with get_db_session() as session:
        yield session


async def get_db():

    async with get_session() as session:
        yield session


Base = declarative_base()
