import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .Models import (
    User,
    Question,
    UserAnswer,
    QuestionType,
    QuestionAnswer
)

dotenv.load_dotenv()

engine = create_engine(f"postgresql+psycopg2://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_HOST_PORT")}/{os.getenv("DB_NAME")}")
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))