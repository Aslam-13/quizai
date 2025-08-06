from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class TrueFalse(Base):
    __tablename__ = "true_false"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Boolean, nullable=False)