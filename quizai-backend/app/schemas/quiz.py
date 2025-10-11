 
from pydantic import BaseModel
from typing import List, Literal, Union

# Request schema
class QuizRequest(BaseModel):
    topic: str
    num_questions: int

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

