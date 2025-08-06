from pydantic import BaseModel

class TrueFalseBase(BaseModel):
    question: str
    answer: bool  # true or false

class TrueFalseCreate(TrueFalseBase):
    pass

class TrueFalseRead(TrueFalseBase):
    id: int

    class Config:
        orm_mode = True