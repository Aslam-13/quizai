from sqlalchemy import Column, Integer, String
from app.db.base import Base

class MCQMultiple(Base):
    __tablename__ = "mcqs_multiple"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answers = Column(String, nullable=False)