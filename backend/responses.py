from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    topics: set[str]
    question_type: str
    question: str
    paper: int
    year: int
    question_number: str
    marks: int
    answer_areas: Optional[list[str]] = None
    answer: list[str|list[str]]
