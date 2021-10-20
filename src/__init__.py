from flask_cors import CORS

from .app import app
from src.routes import auth
from src.routes import articles
from src.routes import serve_redoc

CORS(app)
app.register_blueprint(articles.router)
app.register_blueprint(auth.router)
app.register_blueprint(serve_redoc.router)
