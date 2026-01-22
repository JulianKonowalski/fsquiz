import json

from flask import Blueprint 
from db import Question, QuestionAnswer, SessionLocal

questions_blueprint: Blueprint = Blueprint("questions", __name__, url_prefix="/questions")

# ------------------------------------------------------------------------------------------------ #

@questions_blueprint.route("/", methods=["GET"])
def getQuestions():
    session = SessionLocal()
    return json.dumps({
        "questions": [{
            "id": question.id,
            "text": question.text,
            "category": question.category,
            "type": question.type_id
        } for question in session
            .query(Question)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #

@questions_blueprint.route("/<int:question_id>", methods=["GET"])
def getQuestionByID(question_id: int):
    session = SessionLocal()
    question: Question = session.query(Question).where(Question.id == question_id).one()
    return json.dumps({
        "questions": {
            "id": question.id,
            "text": question.text,
            "category": question.category,
            "type": question.type_id
        }
    })

# ------------------------------------------------------------------------------------------------ #

@questions_blueprint.route("/categories", methods=["GET"])
def getQuestionCategories():
    session = SessionLocal()
    return json.dumps({
        "categories": [
            category[0] for category in session
                .query(Question.category)
                .distinct()
                .all()
        ]
    })

# ------------------------------------------------------------------------------------------------ #

@questions_blueprint.route("/categories/<category>", methods=["GET"])
def getQuestionsByCategory(category: str | int):
    session = SessionLocal()
    return json.dumps({
        "questions": [{
            "id": question.id,
            "text": question.text,
            "category": question.category,
            "type": question.type_id
        } for question in session
            .query(Question)
            .where(Question.category == category)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #

@questions_blueprint.route("/<int:question_id>/answers", methods=["GET"])
def getQuestionAnswers(question_id: int):
    session = SessionLocal()
    return json.dumps({
        "answers": [{
            "id": answer.id,
            "text": answer.text,
            "is_correct": answer.is_correct,
            "question_id": answer.question_id
        } for answer in session
            .query(QuestionAnswer)
            .where(QuestionAnswer.question_id == question_id)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #