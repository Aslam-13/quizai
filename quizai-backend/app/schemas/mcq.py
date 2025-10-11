# app/schemas/mcq.py
from pydantic import BaseModel

class MCQBase(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

class MCQCreate(MCQBase):
    pass

class MCQRead(MCQBase):
    id: int

    class Config:
        orm_mode = True
        