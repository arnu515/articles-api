from functools import wraps
from inspect import getfullargspec
from typing import Callable

from donttrust import DontTrust, ValidationError
from flask import request

from src.util.exceptions import HTTPException
from src.util.jsonwebtoken import get_user


def validate_body(trust: DontTrust):
    def decorator(f: Callable):
        @wraps(f)
        def decorated(*args, **kwargs):
            body = request.json or request.form
            if body is None:
                raise HTTPException("Please provide a request body", 422)
            try:
                trust.validate(body)
            except ValidationError as e:
                raise HTTPException(e.message, 400, {
                    "message": e.message,
                    "field": e.field
                })
            # Check if the function wants the body parameter.
            # If it does, send it
            if "body" in getfullargspec(f).args:
                kwargs["body"] = body
            return f(*args, **kwargs)
        return decorated
    return decorator


def login_required(optional_or_f=False):
    optional = True if type(optional_or_f) != bool else optional_or_f

    def decorator(f: Callable):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("x-token")
            if not token:
                auth_header = request.headers.get("Authorization", None)
                if not auth_header:
                    if optional:
                        return f(*args, **kwargs)
                    raise HTTPException("Unauthorized", 401)
                spl = auth_header.split()
                if len(spl) != 2 or spl[0].lower() != "bearer" or not spl[1]:
                    if optional:
                        return f(*args, **kwargs)
                    raise HTTPException("Unauthorized", 401)
                token = spl[1]
            if not token:
                if optional:
                    return f(*args, **kwargs)
                raise HTTPException("Unauthorized", 401)
            user = get_user(token)
            if not user:
                if optional:
                    return f(*args, **kwargs)
                raise HTTPException("Invalid token")

            # Check if the function wants the user parameter.
            # If it does, send it
            if "user" in getfullargspec(f).args:
                kwargs["user"] = user
            return f(*args, **kwargs)
        return decorated
    if callable(optional_or_f):
        return decorator(optional_or_f)
    return decorator
