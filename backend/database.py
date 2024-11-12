import psycopg2

from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
from http import HTTPStatus

from authenticator import Authenticator
from payloads import RegisterForm, LoginForm
from user import User

class DataBase:

    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

        load_dotenv()

        self.connection = psycopg2.connect(
            host=getenv('DB_URL'),
            port=getenv('DB_PORT'),
            database = getenv('DB_NAME'),
            user = getenv('DB_USER'),
            password = getenv('DB_PASSWORD')
        )
        self.cursor = self.connection.cursor()

        self.get_version()

    def get_user(self, username=None, id=None) -> User | None:
        """Interrogate the database to obtain User | None using the username | id"""
        if username is not None:
            self.cursor.execute("SELECT * FROM users WHERE username=%s;", (username, ))
        elif id is not None:
            self.cursor.execute("SELECT * FROM users WHERE id=%s;", (id, ))
        else: return None
        return User(self.cursor.fetchone())

    def create_user(self, registerForm: RegisterForm):
        """Insert User into the database using a RegisterForm"""
        self.cursor.execute(
            "INSERT INTO users (first_name, last_name, username, password) \
            VALUES (%s, %s, %s, %s) RETURNING id;", registerForm.insert_params(self.authenticator))
        
        self.connection.commit()

        return self.authenticator.create_jwt_token(registerForm.get_token())

    def login_user(self, loginForm: LoginForm) -> str:
        """Login/Authenticate user using a LoginForm"""
        user = self.get_user(username=loginForm.username)
        if user and self.authenticator.check_password(loginForm.password, user.password):
            return self.authenticator.create_jwt_token(user.get_token())
        
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect username or password")

    def get_version(self):
        """Get the Database Version"""
        self.cursor.execute("SELECT version();")
        db_version = self.cursor.fetchone()
        print(db_version)

    def close(self):
        """Close the Cursor and Connection"""
        self.cursor.close()
        self.connection.close()