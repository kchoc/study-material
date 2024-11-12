from fastapi import Request
from http import HTTPStatus

class ErrorResponse:
    def __init__(self, message, status):
        self.message = message
        self.status = status

class ErrorUtil:
    def formContainsKeys(self, json: dict, keys: list[str]) -> ErrorResponse | None:
        for key in keys:
            if key not in json:
                return ErrorResponse(f"Missing {key} in json application.", HTTPStatus.BAD_REQUEST)