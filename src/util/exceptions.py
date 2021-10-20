from typing import Optional

from flask import make_response, jsonify


class HTTPException(Exception):
    message: str
    status: int
    data: dict

    def __init__(self, message: str, status = 400, data: Optional[dict] = None):
        self.message = message
        self.status = status
        self.data = data or {}

    @property
    def response(self):
        return make_response(jsonify(dict(
            message=self.message,
            data=self.data
        )), self.status)
