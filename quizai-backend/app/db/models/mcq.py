from sqlalchemy import Column, Integer, String
from app.db.base import Base

class MCQ(Base):
    __tablename__ = "mcqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)  