from fastapi import FastAPI

from database import DataBase

from endpoints.auth import Auth
from endpoints.resources import CSResources

class Router:
    def __init__(self, app: FastAPI, database: DataBase) -> None:
        self.auth = Auth(app, database)
        self.cs_resources = CSResources(app, database)
