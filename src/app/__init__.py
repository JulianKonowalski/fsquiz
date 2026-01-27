from flask import Flask
from flask_cors import CORS
from db import SessionLocal

from app.users import users_blueprint
from app.questions import questions_blueprint 

def createApp() -> Flask:
    app: Flask = Flask(__name__)

    CORS(app)

    @app.teardown_appcontext
    def removeSession(exception=None):
        SessionLocal.remove()

    app.register_blueprint(users_blueprint)
    app.register_blueprint(questions_blueprint)

    return app