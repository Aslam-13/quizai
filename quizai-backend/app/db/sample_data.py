# app/db/sample_data.py
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import select as sqlmodel_select
from sqlmodel import Relationship
from sqlalchemy.orm import selectinload
from app.db.database import engine, create_db_and_tables
from app.models.quiz_models import Chat, Quiz, MCQQuestion, MultiMCQQuestion, FillBlankQuestion, TrueFalseQuestion
from datetime import datetime
import os
import logging
import asyncio

# Configure logging to see potential errors more clearly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_sample_data():
    """
    Creates sample data for Chat, Quiz, and all question types.
    Checks if data already exists to prevent duplicates on re-runs.
    """
    async with AsyncSession(engine) as session:
        # Check if any chat data already exists
        existing_chat = (await session.exec(sqlmodel_select(Chat))).first()
        if existing_chat:
            logger.info("Sample data already exists. Skipping creation.")
            return

        logger.info("Creating sample data...")

        try:
            # 1. Create a Chat session
            chat1 = Chat()
            session.add(chat1)
            await session.commit()
            await session.refresh(chat1) # Refresh to get the ID
            logger.info(f"Created Chat with ID: {chat1.id}")

            # 2. Create a Quiz for the Chat
            quiz1 = Quiz(
                topic_name="Python Basics",
                num_questions=4,
                chat_id=chat1.id,
                version=1
            )
            session.add(quiz1)
            await session.commit()
            await session.refresh(quiz1)
            logger.info(f"Created Quiz '{quiz1.topic_name}' (ID: {quiz1.id}) for Chat: {quiz1.chat_id}")

            # 3. Create Questions for Quiz 1
            mcq1 = MCQQuestion(
                q="What is the output of `2 + 2` in Python?",
                options=["3", "4", "5", "22"],
                ans="4",
                explain="In Python, `2 + 2` performs integer addition, resulting in 4.",
                quiz_id=quiz1.id
            )
            multi_mcq1 = MultiMCQQuestion(
                q="Which of these are valid ways to comment in Python?",
                options=["// comment", "# comment", "/* comment */", "'''comment'''"],
                ans=["# comment", "'''comment'''"],
                explain="Comments in Python use '#' for single-line and triple quotes for multi-line.",
                quiz_id=quiz1.id,
            )
            fill_blank1 = FillBlankQuestion(
                q="The keyword used to define a function in Python is ____.",
                ans="def",
                explain="`def` is used to define functions in Python.",
                quiz_id=quiz1.id
            )
            true_false1 = TrueFalseQuestion(
                q="Python is a statically typed language.",
                ans=False,
                explain="Python is a dynamically typed language, meaning type checking happens at runtime.",
                quiz_id=quiz1.id
            )

            session.add(mcq1)
            session.add(multi_mcq1)
            session.add(fill_blank1)
            session.add(true_false1)
            await session.commit()
            await session.refresh(mcq1)
            await session.refresh(multi_mcq1)
            await session.refresh(fill_blank1)
            await session.refresh(true_false1)
            logger.info(f"Added 4 questions for Quiz: {quiz1.id}")

            # 4. Create another Quiz for the same Chat (e.g., a more difficult version)
            quiz2 = Quiz(
                topic_name="Python Advanced",
                num_questions=1,
                chat_id=chat1.id,
                version=1
            )
            session.add(quiz2)
            await session.commit()
            await session.refresh(quiz2)
            logger.info(f"Created Quiz '{quiz2.topic_name}' (ID: {quiz2.id}) for Chat: {chat1.id}")

            # 5. Add a question to Quiz 2
            mcq2 = MCQQuestion(
                q="What is a decorator in Python?",
                options=["A design pattern", "A function that takes another function and extends its behavior", "A type of class", "A built-in module"],
                ans="A function that takes another function and extends its behavior",
                explain="A decorator is a design pattern that allows you to add new functionality to an existing object without modifying its structure.",
                quiz_id=quiz2.id
            )
            session.add(mcq2)
            await session.commit()
            await session.refresh(mcq2)
            logger.info(f"Added 1 question for Quiz: {quiz2.id}")

            logger.info("All sample data committed to database.")

        except Exception as e:
            await session.rollback() # Ensure rollback on error
            logger.error(f"An error occurred during sample data creation: {e}", exc_info=True)
            raise # Re-raise the exception after logging

        # After commit, refresh objects if you need to access relationships that were loaded lazily
        await session.refresh(chat1)

# Example of how to run this when your application starts
async def main():
    logger.info("Initializing database...")
    await create_db_and_tables() # Create tables if they don't exist
    await create_sample_data()   # Populate with sample data

    # Optional: Example of querying the created data
    # async with AsyncSession(engine) as session:
    #     logger.info("\n--- Querying Sample Data ---")
    #     try:
    #         chats = (await session.exec(sqlmodel_select(Chat).options(selectinload(Chat.quizzes)))).all()
    #         if not chats:
    #             logger.warning("No chats found in the database after creation.")
    #         for chat in chats:
    #             logger.info(f"Chat ID: {chat.id}, Created At: {chat.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    #             for quiz in chat.quizzes:
    #                 # Eagerly load relationships for querying each quiz
    #                 quiz_with_questions = (await session.exec(
    #                     sqlmodel_select(Quiz).where(Quiz.id == quiz.id).options(
    #                         selectinload(Quiz.mcqs),
    #                         selectinload(Quiz.multi_mcqs),
    #                         selectinload(Quiz.fill_blanks),
    #                         selectinload(Quiz.true_false_questions)
    #                     )
    #                 )).first()

    #                 if quiz_with_questions:
    #                     logger.info(f"  Quiz ID: {quiz_with_questions.id}, Topic: {quiz_with_questions.topic_name}, Version: {quiz_with_questions.version}, Num Questions: {quiz_with_questions.num_questions}")
    #                     logger.info("    MCQs:")
    #                     for mcq in quiz_with_questions.mcqs:
    #                         logger.info(f"      - Q: {mcq.q}, Ans: {mcq.ans}, Options: {mcq.options}")
    #                     logger.info("    MultiMCQs:")
    #                     for multi_mcq in quiz_with_questions.multi_mcqs:
    #                         logger.info(f"      - Q: {multi_mcq.q}, Ans: {multi_mcq.ans}, Options: {multi_mcq.options}")
    #                     logger.info("    Fill Blanks:")
    #                     for fb in quiz_with_questions.fill_blanks:
    #                         logger.info(f"      - Q: {fb.q}, Ans: {fb.ans}")
    #                     logger.info("    True/False:")
    #                     for tf in quiz_with_questions.true_false_questions:
    #                         logger.info(f"      - Q: {tf.q}, Ans: {tf.ans}")
    #     except Exception as e:
    #         await session.rollback() # Rollback the query session if an error occurs
    #         logger.error(f"An error occurred during sample data querying: {e}", exc_info=True)
    #         raise # Re-raise the exception after logging

if __name__ == "__main__":
    asyncio.run(main())