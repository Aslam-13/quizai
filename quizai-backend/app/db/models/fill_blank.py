from sqlalchemy import Column, Integer, String
from app.db.base import Base

class FillBlank(Base):
    __tablename__ = "fill_blanks"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)