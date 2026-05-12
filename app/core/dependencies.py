import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal, redis_client


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    yield redis_client
