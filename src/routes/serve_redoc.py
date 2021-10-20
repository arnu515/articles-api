from flask import Blueprint, send_file
from os.path import join, abspath, dirname

router = Blueprint("serve_redoc", __name__)


@router.get("/openapi.yaml")
def serve_openapi_yaml():
    return send_file(join(dirname(abspath(__file__)), "../../openapi.yaml"))


@router.get("/docs")
def serve_redoc():
    with open(join(dirname(abspath(__file__)), "../../redoc-static.html")) as f:
        return f.read()
