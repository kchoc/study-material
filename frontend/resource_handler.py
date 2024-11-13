import json
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


class ResourceHandler:
    def __init__(self):
        self.questions: list[Question] = self.load_list_resource("./backend/resources/computer_science/questions.json", type=Question)
    
    def load_list_resource(self, filename: str, type: type = None):
        with open(filename, "r") as file:
            items = json.loads(file.read())
        
        if type is None:
            return items
        
        serialized_items = []
        for item in items:
            serialized_items.append(type(**item))
        return serialized_items