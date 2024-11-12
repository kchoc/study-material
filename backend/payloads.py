from pydantic import BaseModel

from authenticator import Authenticator

class LoginForm(BaseModel):
    username: str
    password: str

class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

    def get_token(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def insert_params(self, authenticator: Authenticator):
        return (self.first_name, self.last_name, self.username, authenticator.hash_password(self.password))

class QuestionQueryForm(BaseModel):
    question_papers: set[int]
    years: set[int]
    topics: set[str]