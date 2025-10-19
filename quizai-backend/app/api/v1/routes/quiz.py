from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.quiz import QuizRequest, QuizResponse
from app.services.ai import generate_quiz
from app.services.quiz_crud import save_quiz_to_db
from app.db.database import get_async_session
from app.models.quiz_models import QuizSummary
from sqlmodel import select

router = APIRouter()

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz_endpoint(
    payload: QuizRequest,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        quiz_summary_string = None
        if payload.version >= 2 and payload.summary_id:
            quiz_summary = await session.exec(select(QuizSummary).where(QuizSummary.id == payload.summary_id))
            quiz_summary_obj = quiz_summary.first()
            if quiz_summary_obj:
                quiz_summary_string = quiz_summary_obj.summary_string

        quiz_response = await generate_quiz(payload.topic, payload.num_questions, payload.version, quiz_summary_string)
        await save_quiz_to_db(session, payload.topic, payload.num_questions, payload.version, quiz_response, payload.chat_id, quiz_summary_string)
        return quiz_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

