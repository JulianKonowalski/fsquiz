import os
import json
import dotenv

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from db.Models import *

dotenv.load_dotenv()

DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_HOST_PORT")
DB_NAME = os.getenv("DB_NAME")

app: Flask = Flask(__name__)
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

@app.route("/questions", methods=["GET"])
def getQuestions():
    questions: list[Question] = SessionLocal().query(Question).all()
    return app.response_class(
        response=json.dumps({
            "questions": [{
                "id": question.id,
                "text": question.text,
                "category": question.category,
                "type": question.type_id
            } for question in questions]
        }),
        status=200,
        mimetype="application/json"
    )

@app.route("/questions/<question_id>/answers", methods=["GET"])
def getQuestionAnswers(question_id: int):
    try: question_id = int(question_id)
    except ValueError: return app.make_response("Parameter question_id should be an integer", 400)

    answers: list[QuestionAnswer] = SessionLocal().query(QuestionAnswer).filter(QuestionAnswer.question_id == question_id).all()
    return app.response_class(
        response=json.dumps({
            "answers": [{
                "id": answer.id,
                "text": answer.text,
                "is_correct": answer.is_correct,
                "question_id": answer.question_id
            } for answer in answers]
        }),
        status=200,
        mimetype="application/json"
    )

@app.route("/users/create_user", methods=["POST"])
def createUser():
    # api key authorization here
    # TODO
    pass

@app.route("/users/authorize_user", methods=["POST"])
def autorizeUser():
    # api key authorization here
    # TODO
    pass

@app.route("/users/answers/create", methods=["POST"])
def createUserAnswer():
    # api key authorization here
    # TODO
    pass

@app.route("/users/answers/<user_id>", methods=["GET"])
def getUserAnswers(user_id: int):
    try: user_id = int(user_id)
    except ValueError: return app.make_response("Parameter question_id should be an integer", 400)
    
    # api key authorization here
    # TODO

    user_answers: list[UserAnswer] = SessionLocal().query(UserAnswer).filter(UserAnswer.user_id == user_id).all()
    return app.response_class(
        response=json.dumps({
            "user_answers": [{
                "id": user_answer.id,
                "user_id": user_answer.user_id,
                "question_id": user_answer.question_id,
                "answer_id": user_answer.answer_id
            } for user_answer in user_answers]
        }),
        status=200,
        mimetype="application/json"
    )

@app.teardown_appcontext
def removeSession(exception=None):
    SessionLocal.remove()

app.run(host="0.0.0.0", port=5000, debug=False)