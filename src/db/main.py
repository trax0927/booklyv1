from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from src.config import Config
from src.books.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    future=True,
)

async def init_db():
        async with async_engine.begin() as conn:
          await conn.run_sync(SQLModel.metadata.create_all)



async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
        
    async with Session() as session:
        yield session