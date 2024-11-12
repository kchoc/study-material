from fastapi import HTTPException

from http import HTTPStatus
from endpoints.endpoint import Endpoint
from payloads import LoginForm, RegisterForm

class Auth(Endpoint):
    def __init__(self, *args):
        super().__init__(*args)

        @self.app.post('/register')
        async def register(registerForm: RegisterForm):
            # Check if user already exists
            if self.database.get_user(username=registerForm.username):
                raise HTTPException(HTTPStatus.CONFLICT, "User already Exists!")
            
            # Create user if one does not exist
            return self.database.create_user(registerForm)


        @self.app.post('/login')
        async def login(login: LoginForm) -> str:
            user = self.database.login_user(login)
            
            return user