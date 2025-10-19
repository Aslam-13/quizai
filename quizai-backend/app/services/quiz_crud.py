from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.quiz_models import (
    Chat,
    Quiz,
    MCQQuestion,
    MultiMCQQuestion,
    FillBlankQuestion,
    TrueFalseQuestion,
    QuizSummary
)
from app.schemas.quiz import QuizResponse, MCQ, MultiMCQ, FillBlank, TrueFalse

async def get_chat_by_id(session: Session, chat_id: UUID) -> Optional[Chat]:
    statement = select(Chat).where(Chat.id == chat_id)
    result = await session.exec(statement)
    return result.scalar_one_or_none()

async def create_chat(session: Session) -> Chat:
    chat = Chat()
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return chat

async def create_quiz(
    session: Session,
    topic: str,
    num_questions: int,
    version: int,
    chat_id: UUID,
) -> Quiz:
    quiz = Quiz(
        topic_name=topic,
        num_questions=num_questions,
        version=version,
        chat_id=chat_id,
    )
    session.add(quiz)
    await session.commit()
    await session.refresh(quiz)
    return quiz

async def create_mcq_questions(
    session: Session, mcqs: List[MCQ], quiz_id: UUID
) -> List[MCQQuestion]:
    db_mcqs = []
    for mcq_data in mcqs:
        db_mcq = MCQQuestion(
            q=mcq_data.q,
            options=mcq_data.options,
            ans=mcq_data.ans,
            explain=mcq_data.explain,
            quiz_id=quiz_id,
        )
        db_mcqs.append(db_mcq)
        session.add(db_mcq)
    await session.commit()
    for db_mcq in db_mcqs:
        await session.refresh(db_mcq)
    return db_mcqs

async def create_multi_mcq_questions(
    session: Session, multi_mcqs: List[MultiMCQ], quiz_id: UUID
) -> List[MultiMCQQuestion]:
    db_multi_mcqs = []
    for multi_mcq_data in multi_mcqs:
        db_multi_mcq = MultiMCQQuestion(
            q=multi_mcq_data.q,
            options=multi_mcq_data.options,
            ans=multi_mcq_data.ans,
            explain=multi_mcq_data.explain,
            quiz_id=quiz_id,
        )
        db_multi_mcqs.append(db_multi_mcq)
        session.add(db_multi_mcq)
    await session.commit()
    for db_multi_mcq in db_multi_mcqs:
        await session.refresh(db_multi_mcq)
    return db_multi_mcqs

async def create_fill_blank_questions(
    session: Session, fill_blanks: List[FillBlank], quiz_id: UUID
) -> List[FillBlankQuestion]:
    db_fill_blanks = []
    for fill_blank_data in fill_blanks:
        db_fill_blank = FillBlankQuestion(
            q=fill_blank_data.q,
            ans=fill_blank_data.ans,
            explain=fill_blank_data.explain,
            quiz_id=quiz_id,
        )
        db_fill_blanks.append(db_fill_blank)
        session.add(db_fill_blank)
    await session.commit()
    for db_fill_blank in db_fill_blanks:
        await session.refresh(db_fill_blank)
    return db_fill_blanks

async def create_true_false_questions(
    session: Session, true_false_questions: List[TrueFalse], quiz_id: UUID
) -> List[TrueFalseQuestion]:
    db_true_false_questions = []
    for tf_data in true_false_questions:
        db_tf_question = TrueFalseQuestion(
            q=tf_data.q,
            ans=tf_data.ans == "True",  # Convert "True"/"False" string to boolean
            explain=tf_data.explain,
            quiz_id=quiz_id,
        )
        db_true_false_questions.append(db_tf_question)
        session.add(db_tf_question)
    await session.commit()
    for db_tf_question in db_true_false_questions:
        await session.refresh(db_tf_question)
    return db_true_false_questions

async def save_quiz_to_db(
    session: Session,
    topic: str,
    num_questions: int,
    version: int,
    quiz_response: QuizResponse,
    chat_id: Optional[UUID] = None,
    quiz_summary_string: Optional[str] = None,
) -> Quiz:
    if chat_id:
        chat = await get_chat_by_id(session, chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found.")
    else:
        chat = await create_chat(session)

    quiz = await create_quiz(session, topic, num_questions, version, chat.id)

    if version >= 2 and quiz_summary_string:
        quiz_summary = QuizSummary(
            quiz_id=quiz.id,
            summary_string=quiz_summary_string,
            version=version
        )
        session.add(quiz_summary)
        await session.commit()
        await session.refresh(quiz_summary)

    await create_mcq_questions(session, quiz_response.mcq, quiz.id)
    await create_multi_mcq_questions(session, quiz_response.multi_mcq, quiz.id)
    await create_fill_blank_questions(session, quiz_response.fillblanks, quiz.id)
    await create_true_false_questions(session, quiz_response.true_false, quiz.id)

    return quiz
