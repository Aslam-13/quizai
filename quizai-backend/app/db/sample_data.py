# app/db/sample_data.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.mcq import MCQ
from app.db.models.fill_blank import FillBlank
from app.db.models.mcq_multiple import MCQMultiple
from app.db.models.true_false import TrueFalse
from app.db.base import Base  # Import your Base
from app.db.session import engine  # Import your engine

async def ensure_tables_exist():
    """Create all tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables ensured to exist")

async def insert_sample_data(db: AsyncSession):
    # Create tables first if they don't exist
    await ensure_tables_exist()
    
    # Your existing sample data
    mcq = MCQ(
        question="What is the capital of France?",
        option_a="Berlin",
        option_b="Madrid",
        option_c="Paris",
        option_d="Rome",
        correct_answer="C"
    )

    fill = FillBlank(
        question="The chemical symbol for water is ___",
        answer="H2O"
    )

    mcq_multiple = MCQMultiple(
        question="Which of the following are programming languages?",
        option_a="Python",
        option_b="HTML",
        option_c="Java",
        option_d="CSS",
        correct_answers="A,C"
    )

    tf = TrueFalse(
        question="The sun rises in the west.",
        answer=False
    )

    # Add all data
    db.add_all([mcq, fill, mcq_multiple, tf])
    await db.commit()
    print("✅ Sample data inserted.")