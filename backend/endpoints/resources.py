from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from endpoints.endpoint import Endpoint
from resource_loader import load_list_resource
from payloads import QuestionQueryForm
from responses import Question

class CSResources(Endpoint):
    def __init__(self, *args):
        super().__init__(*args)
        self.questions: list[Question] = load_list_resource("./backend/resources/computer_science/questions.json", type=Question)

        @self.app.post('/computerScience/resources/querySelectQuestions')
        async def query_select_questions(question_query_form: QuestionQueryForm):
            response = []
            for question in self.questions:
                if question.paper in question_query_form.question_papers and \
                    bool(question.topics & question_query_form.topics) and \
                    question.year in question_query_form.years:
                    response.append(question)
            
            return response