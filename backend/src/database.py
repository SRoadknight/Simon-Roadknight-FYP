import os
from dotenv import load_dotenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


load_dotenv()
db_url = os.getenv('DATABASE_URL')

async_engine = create_async_engine(db_url, echo=True, future=True)  

async def get_session():
    async with AsyncSession(async_engine) as session:
        yield session