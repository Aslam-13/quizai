from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine # Correct import for create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession # This import is correct
from sqlalchemy import text
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Using SQLite for simplicity. You can change this to PostgreSQL, MySQL, etc.
# The database file 'quizai.db' will be created in the project root.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure your database connection.")

engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    """Creates all defined tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get an asynchronous database session."""
    async with AsyncSession(engine) as session:
        yield session

async def test_db_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            return {"db_status": "connected", "result": result.scalar()}
    except Exception as e:
        return {"db_status": "error", "error": str(e)}