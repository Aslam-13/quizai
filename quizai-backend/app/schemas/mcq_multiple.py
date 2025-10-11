from pydantic import BaseModel

class MCQMultipleBase(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answers: str  # e.g., "A,C"

class MCQMultipleCreate(MCQMultipleBase):
    pass

class MCQMultipleRead(MCQMultipleBase):
    id: int

    class Config:
        orm_mode = True
        