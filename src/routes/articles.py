from donttrust import DontTrust, Schema
from flask import Blueprint, make_response, jsonify, request
from prisma.models import User

from src.db import db
from src.util.decorators import validate_body, login_required
from src.util.exceptions import HTTPException

router = Blueprint("articles", __name__, url_prefix="/api/articles")


@router.get("")
def get_articles():
    return make_response(jsonify(list(map(lambda x: x.dict(), db.article.find_many(include={"author": True})))))


@router.get("<string:id>")
def get_article(id: str):
    article = db.article.find_first(where={"id": id}, include={"author": True})
    if not article:
        raise HTTPException("Article not found", 404)
    return make_response(jsonify(article.dict()))


@router.post("")
@validate_body(DontTrust(
    title=Schema().string().required(),
    content=Schema().string().required()
))
@login_required
def create_article(user: User):
    body = request.form or request.json
    article = db.article.create({
        "title": body.get("title").strip(),
        "content": body.get("content").strip(),
        "user_id": user.id
    }, include={"author": True})

    return make_response(jsonify(article.dict()), 201)


@router.put("<string:id>")
@validate_body(DontTrust(
    title=Schema().string(),
    content=Schema().string()
))
@login_required
def update_article(id: str, user: User):
    body = request.form or request.json
    article = db.article.find_first(where={
        "id": id
    })
    if not article:
        raise HTTPException("Article not found", 404)
    if article.user_id != user.id:
        raise HTTPException("Forbidden", 403)
    article = db.article.update(data={
        "title": body.get("title").strip(),
        "content": body.get("content").strip(),
    }, where={"id": id}, include={"author": True})
    return make_response(jsonify(article.dict()), 201)


@router.delete("<string:id>")
@validate_body(DontTrust(
    title=Schema().string(),
    content=Schema().string()
))
@login_required
def delete_article(id: str, user: User):
    article = db.article.find_first(where={
        "id": id
    })
    if not article:
        raise HTTPException("Article not found", 404)
    if article.user_id != user.id:
        raise HTTPException("Forbidden", 403)
    db.article.delete(where={"id": id})
    return make_response(jsonify({}), 204)
