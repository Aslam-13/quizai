from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship, JSON, Column

# Base model for common fields like ID and timestamps
class TimestampedModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})

# Chat Model (Grandparent)
class Chat(TimestampedModel, table=True):
    __tablename__ = "chats"
    quizzes: List["Quiz"] = Relationship(back_populates="chat")

# Quiz Model (Parent)
class Quiz(TimestampedModel, table=True):
    __tablename__ = "quizzes"
    topic_name: str = Field(index=True)
    version: int = Field(default=1)
    num_questions: int
    chat_id: UUID = Field(foreign_key="chats.id")

    chat: Chat = Relationship(back_populates="quizzes")
    summaries: List["QuizSummary"] = Relationship(back_populates="quiz")
    mcqs: List["MCQQuestion"] = Relationship(back_populates="quiz")
    multi_mcqs: List["MultiMCQQuestion"] = Relationship(back_populates="quiz")
    fill_blanks: List["FillBlankQuestion"] = Relationship(back_populates="quiz")
    true_false_questions: List["TrueFalseQuestion"] = Relationship(back_populates="quiz")

# Quiz Summary Model
class QuizSummary(TimestampedModel, table=True):
    __tablename__ = "quiz_summaries"
    quiz_id: UUID = Field(foreign_key="quizzes.id")
    summary_string: str
    version: int = Field(default=1)

    quiz: Quiz = Relationship(back_populates="summaries")

# Question Base Model (not a table itself, for inheritance)
class QuestionBase(TimestampedModel):
    q: str
    explain: str
    quiz_id: UUID = Field(foreign_key="quizzes.id")
    # The 'quiz' relationship will be defined in concrete question models with specific back_populates

# MCQ Question Model
class MCQQuestion(QuestionBase, table=True):
    __tablename__ = "mcq_questions"
    options: List[str] = Field(sa_column=Column(JSON)) # SQLModel's JSON type handles serialization/deserialization
    ans: str

    quiz: Quiz = Relationship(back_populates="mcqs")

# MultiMCQ Question Model
class MultiMCQQuestion(QuestionBase, table=True):
    __tablename__ = "multi_mcq_questions"
    options: List[str] = Field(sa_column=Column(JSON))
    ans: List[str] = Field(sa_column=Column(JSON))

    quiz: Quiz = Relationship(back_populates="multi_mcqs")

# FillBlank Question Model
class FillBlankQuestion(QuestionBase, table=True):
    __tablename__ = "fill_blank_questions"
    ans: str

    quiz: Quiz = Relationship(back_populates="fill_blanks")

# TrueFalse Question Model
class TrueFalseQuestion(QuestionBase, table=True):
    __tablename__ = "true_false_questions"
    ans: bool # Store as boolean

    quiz: Quiz = Relationship(back_populates="true_false_questions")
