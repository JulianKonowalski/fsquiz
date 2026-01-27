import os
import sys
import json
import dotenv
import pathlib

from typing import Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.db.Models import *

def getData() -> Tuple[list[Question], list[QuestionAnswer]]:
    DATA_PATH: pathlib.Path = pathlib.Path(__file__).parent.joinpath("../data/questions.json").resolve()
    with open(DATA_PATH, "r") as file: data: dict = json.loads(file.read())["questions"]

    questions: list[Question]       = []
    answers: list[QuestionAnswer]   = []
    global_answer_index: int = 1
    for question_index, question in enumerate(data):
        questions.append(Question(
            id          = question_index + 1,
            text        = question["text"],
            category    = question["category"],
            difficulty  = question["difficulty"],
            type_id     = question["type"]
        ))

        answers += [QuestionAnswer(
            id          = global_answer_index + local_answer_index,
            text        = answer,
            is_correct  = local_answer_index == question["correctAnswers"] if question["type"] == "single-choice" else local_answer_index in question["correctAnswers"],
            question_id = question_index + 1
        ) for local_answer_index, answer in enumerate(question["answers"])]

        global_answer_index += len(question["answers"])

    return (questions, answers)

if __name__ == "__main__":
    questions, answers = getData()
    
    dotenv.load_dotenv()

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USERNAME")
    DB_PASS = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_HOST_PORT")

    DB_URL_BASE     = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
    DB_URL_ADMIN    = f"{DB_URL_BASE}/postgres"
    DB_URL_TMP      = f"{DB_URL_BASE}/tmp"
    DB_URL_TARGET   = f"{DB_URL_BASE}/{DB_NAME}"

    admin_engine = create_engine(DB_URL_ADMIN, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as connection:
        connection.execute(text("CREATE DATABASE tmp"))
        connection.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
        connection.execute(text("DROP DATABASE tmp"))
    
    target_engine = create_engine(DB_URL_TARGET)
    Base.metadata.create_all(target_engine)
    
    Session = sessionmaker(bind=target_engine)
    session = Session()
    session.add_all([QuestionType(id="multi-choice"), QuestionType(id="single-choice")])
    session.add_all(questions)
    session.add_all(answers)
    session.commit()