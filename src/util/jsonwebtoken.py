from os import getenv
from typing import Optional

import jwt
from prisma.models import User

from src.db import db

SECRET = getenv("SECRET", "secret")


def generate(user: User) -> str:
    return jwt.encode({"id": user.id}, SECRET, algorithm="HS256")


def get_user(token: str) -> Optional[User]:
    try:
        identity = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.user.find_first(where={"id": identity.get("id")})
        return user or None
    except jwt.exceptions.PyJWTError:
        return None
