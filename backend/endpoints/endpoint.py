from fastapi import FastAPI
from database import DataBase

class Endpoint:
    def __init__(self, app: FastAPI, database: DataBase):
        self.app = app
        self.database = database