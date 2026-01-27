from sqlalchemy import Column, ForeignKey 
from sqlalchemy import Text, String, Integer, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ------------------------------------------------------------------------------------------------ #

class QuestionType(Base):

    id: Column      = Column(String(16), primary_key=True, nullable=False)

    __tablename__ = "question_types"

# ------------------------------------------------------------------------------------------------ #

class Question(Base):

    id: Column          = Column(Integer, primary_key=True)
    text: Column        = Column(Text, unique=False, nullable=False)
    category: Column    = Column(String(8), unique=False, nullable=False)
    difficulty: Column  = Column(String(8), unique=False, nullable=False)
    type_id: Column     = Column(String(16), ForeignKey("question_types.id", ondelete="RESTRICT"), nullable=False)

    __tablename__   = "questions"
    type            = relationship("QuestionType")
    answers         = relationship("QuestionAnswer", cascade="all, delete", back_populates="question")

# ------------------------------------------------------------------------------------------------ #

class QuestionAnswer(Base):

    id: Column          = Column(Integer, primary_key=True)
    text: Column        = Column(Text, unique=False, nullable=False)
    is_correct: Column  = Column(Boolean, nullable=False)
    question_id: Column = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    __tablename__   = "question_answers"
    question        = relationship("Question", back_populates="answers")

# ------------------------------------------------------------------------------------------------ #

class User(Base):

    id: Column          = Column(String(16), primary_key=True, nullable=False)
    email: Column       = Column(String(256), unique=False, nullable=False)
    password: Column    = Column(String(32), unique=False, nullable=False)

    __tablename__   = "users"
    answers         = relationship("UserAnswer", cascade="all, delete", back_populates="user")

# ------------------------------------------------------------------------------------------------ #

class UserAnswer(Base):

    id: Column          = Column(Integer, primary_key=True)
    user_id: Column     = Column(String(16), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Column = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    answer_id: Column   = Column(Integer, ForeignKey("question_answers.id", ondelete="CASCADE"), nullable=False)

    __tablename__   = "user_answers"
    user            = relationship("User", back_populates="answers")

# ------------------------------------------------------------------------------------------------ #