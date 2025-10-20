# app/schemas/quiz.py
from typing import List, Literal, Union, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Request schema
class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)
    num_questions: int = Field(..., ge=1, le=20)
    version: int = Field(..., ge=1, le=5)
    chat_id: Optional[UUID] = None
    summary_id: Optional[UUID] = None

# Question types
class MCQ(BaseModel):
    q: str
    options: List[str]
    ans: str
    explain: str

class MultiMCQ(BaseModel):
    q: str
    options: List[str]
    ans: List[str]
    explain: str

class FillBlank(BaseModel):
    q: str
    ans: str
    explain: str

class TrueFalse(BaseModel):
    q: str
    ans: Literal["True", "False"]
    explain: str

# Response schema
class QuizResponse(BaseModel):
    mcq: List[MCQ]
    multi_mcq: List[MultiMCQ]
    fillblanks: List[FillBlank]
    true_false: List[TrueFalse]

# Submission Schema
class Answer(BaseModel):
    question_id: UUID
    submitted_answer: Union[str, List[str], bool]
    question_type: Literal["mcq", "multi_mcq", "fill_blank", "true_false"]

class QuizSubmission(BaseModel):
    quiz_id: UUID
    answers: List[Answer]

