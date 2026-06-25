from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.shared.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session
