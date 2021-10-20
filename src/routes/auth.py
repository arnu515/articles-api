import bcrypt
from donttrust import DontTrust, Schema
from flask import Blueprint, make_response, jsonify
from prisma.models import User

from src.db import db
from src.util.decorators import validate_body, login_required
from src.util.exceptions import HTTPException
from src.util.jsonwebtoken import generate

router = Blueprint("auth", __name__, url_prefix="/api/auth")


@router.post("/login")
@validate_body(DontTrust(
    email=Schema().email().required(),
    password=Schema().string().required()
))
def login_route(body: dict):
    user = db.user.find_first(where={
        "email": body.get("email")
    })
    if user is None:
        raise HTTPException("Invalid username or password", 400)
    if not bcrypt.checkpw(body.get("password").encode(), user.password.encode()):
        raise HTTPException("Invalid username or password", 400)
    token = generate(user)
    return make_response(jsonify({"token": token}))


@router.post("/register")
@validate_body(DontTrust(
    email=Schema().email().required(),
    password=Schema().string().required(),
    username=Schema().string().required()
))
def register_route(body: dict):
    print(body)
    user = db.user.find_first(where={
        "OR": [{"email": body.get("email")}, {"username": body.get("username")}]
    })
    if user is not None:
        raise HTTPException("User already registered. Please log in", 400)
    user = db.user.create({
        "email": body.get("email").strip(),
        "password": bcrypt.hashpw(body.get("password").encode(), bcrypt.gensalt(10)).decode(),
        "username": body.get("username").strip()
    })
    token = generate(user)
    return make_response(jsonify({"token": token}))


@router.get("/user")
@login_required()
def get_user(user: User):
    return make_response(jsonify(user.dict()))
