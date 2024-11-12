import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

from authenticator import Authenticator
from database import DataBase
from router import Router

class Main:
    def __init__(self):
        self.app = FastAPI()

        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.authenticator = Authenticator()
        self.database = DataBase(self.authenticator)

        self.router = Router(self.app, self.database)

        @self.app.get('/teapot')
        def teapot():
            raise HTTPException(HTTPStatus.IM_A_TEAPOT, "I am a teapot")

if __name__ == "__main__":
    main = Main()
    uvicorn.run(main.app, host="0.0.0.0", port=8080)