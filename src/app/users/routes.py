import json

from flask import Blueprint, request
from db import User, UserAnswer, QuestionAnswer, SessionLocal

users_blueprint: Blueprint = Blueprint("users", __name__, url_prefix="/users")

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/", methods=["GET"])
def getUsers():
    session = SessionLocal()
    return json.dumps({
        "users": [{
            "id": user.id,
            "email": user.email,
            "password": user.password
        } for user in session.query(User).all()]
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/<int:user_id>", methods=["GET"])
def getUserByID(user_id: int):
    session = SessionLocal()
    user: User = session.query(User).where(User.id == user_id).one()
    return json.dumps({
        "user": {
            "id": user.id,
            "email": user.email,
            "password": user.password
        }
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/answers/<int:question_id>", methods=["GET"])
def getUserAnswersByQuestionID(question_id: int):
    session = SessionLocal()
    return json.dumps({
        "user_answers": [{
            "id": answer.id,
            "user_id": answer.user_id,
            "question_id": answer.question_id,
            "answer_id": answer.answer_id
        } for answer in session
            .query(UserAnswer)
            .where(UserAnswer.question_id == question_id)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/<int:user_id>/answers", methods=["GET"])
def getUserAnswers(user_id: int):
    session = SessionLocal()
    return json.dumps({
        "user_answers": [{
            "id": answer.id,
            "user_id": answer.user_id,
            "question_id": answer.question_id,
            "answer_id": answer.answer_id
        } for answer in session
            .query(UserAnswer)
            .where(UserAnswer.user_id == user_id)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/<int:user_id>/answers/<int:question_id>", methods=["GET"])
def getUserAnswers(user_id: int, question_id: int):
    session = SessionLocal()
    return json.dumps({
        "user_answers": [{
            "id": answer.id,
            "user_id": answer.user_id,
            "question_id": answer.question_id,
            "answer_id": answer.answer_id
        } for answer in session
            .query(UserAnswer)
            .filter(UserAnswer.user_id == user_id,
                UserAnswer.question_id == question_id)
            .all()]
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/<int:user_id>/answers", methods=["POST"])
def createUserAnswer(user_id: int):
    session = SessionLocal()
    data = request.json()
    success: bool = False
    try:
        answer: UserAnswer = UserAnswer(
            user_id=user_id, 
            question_id=data["question_id"], 
            answer_id=data["answer_id"]
        )
        session.add(answer)
        session.commit()
        success = True
    except:
        session.rollback()
    session.close()
    return json.dumps({
        "status": "success" if success else "failed"
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/<int:user_id>/answers/<int:user_answer_id>", methods=["POST"])
def modifyUserAnswer(user_id: int, user_answer_id: int):
    session = SessionLocal()
    data = request.json()
    success: bool = False
    try:
        user_answer: UserAnswer = session.query(UserAnswer).where(UserAnswer.id == user_answer_id).one()
        if user_answer.user_id != user_id: raise RuntimeError

        user_answer.answer_id = data["answer_id"]
        session.commit()
        success = True
    except:
        session.rollback()
    session.close()
    return json.dumps({
        "status": "success" if success else "failed"
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/create", methods=["POST"])
def createUser():
    session = SessionLocal()
    data = request.json()
    success: bool = False
    try:
        user: User = User(
            id = data["username"],
            email = data["email"],
            password = data["password"]
        )
        session.add(user)
        session.commit()
        success = True
    except:
        session.rollback()
    session.close()
    return json.dumps({
        "status": "success" if success else "failed"
    })

# ------------------------------------------------------------------------------------------------ #

@users_blueprint.route("/authenticate", methods=["POST"])
def authenticateUser():
    session = SessionLocal()
    data = request.json()
    user: User = session.query(User).where(User.id == data["username"]).one()
    return json.dumps({
        "authorized": user.password == data["password"]
    })

# ------------------------------------------------------------------------------------------------ #