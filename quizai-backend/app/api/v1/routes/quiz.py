from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.quiz import QuizRequest, QuizResponse, QuizSubmission, Answer
from app.services.ai import generate_quiz, generate_summary
from app.services.quiz_crud import save_quiz_to_db, get_quiz_with_questions
from app.db.database import get_async_session
from app.models.quiz_models import QuizSummary, MCQQuestion, MultiMCQQuestion, FillBlankQuestion, TrueFalseQuestion
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
        await save_quiz_to_db(session, payload.topic, payload.num_questions, payload.version, quiz_response, payload.chat_id)
        return quiz_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/submit")
async def submit_quiz_endpoint(
    submission: QuizSubmission,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        quiz = await get_quiz_with_questions(session, submission.quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        correct_questions = []
        incorrect_questions = []

        for answer in submission.answers:
            question = None
            if answer.question_type == "mcq":
                question = next((q for q in quiz.mcqs if q.id == answer.question_id), None)
            elif answer.question_type == "multi_mcq":
                question = next((q for q in quiz.multi_mcqs if q.id == answer.question_id), None)
            elif answer.question_type == "fill_blank":
                question = next((q for q in quiz.fill_blanks if q.id == answer.question_id), None)
            elif answer.question_type == "true_false":
                question = next((q for q in quiz.true_false_questions if q.id == answer.question_id), None)

            if not question:
                raise HTTPException(status_code=404, detail=f"Question with ID {answer.question_id} not found in quiz")

            is_correct = False
            if answer.question_type == "mcq" or answer.question_type == "fill_blank":
                is_correct = (answer.submitted_answer == question.ans)
            elif answer.question_type == "multi_mcq":
                # Convert both to sets for order-independent comparison
                is_correct = (set(answer.submitted_answer) == set(question.ans))
            elif answer.question_type == "true_false":
                is_correct = (answer.submitted_answer == question.ans)
            
            if is_correct:
                correct_questions.append(question)
            else:
                incorrect_questions.append(question)
        
        summary_string = await generate_summary(quiz.topic_name, correct_questions, incorrect_questions)

        quiz_summary = QuizSummary(
            quiz_id=quiz.id,
            summary_string=summary_string,
            version=quiz.version + 1 # Increment version for new summary
        )
        session.add(quiz_summary)
        await session.commit()
        await session.refresh(quiz_summary)

        return {"message": "Quiz submitted successfully", "summary_id": quiz_summary.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



