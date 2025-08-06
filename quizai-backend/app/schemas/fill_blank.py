from pydantic import BaseModel

class FillBlankBase(BaseModel):
    question: str
    answer: str

class FillBlankCreate(FillBlankBase):
    pass

class FillBlankRead(FillBlankBase):
    id: int

    class Config:
        orm_mode = True