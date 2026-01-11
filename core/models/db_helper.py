from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings

class DataBaseHelper:
    def __init__(self, url:str):
        self.engine = create_async_engine(
            url=url
        )
        
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )
        

db_helper = DataBaseHelper(url=settings.db_url)