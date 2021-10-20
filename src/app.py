from flask import Flask

from src.util.exceptions import HTTPException
from .db import db

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_http_ex(e: HTTPException):
    return e.response


@app.before_request
def connect_db():
    db.connect()


@app.teardown_request
def close_conn(_):
    if db.is_connected():
        db.disconnect()
