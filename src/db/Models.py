from enum import Enum
from typing import Tuple

class Event:

    id: int | None = None
    name: str | None = None

    def __init__(self, data: Tuple[int, str]):
        self.id = data[0]
        self.name = data[1]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

####################################################################################################

class Quiz:

    id: int | None = None
    event_id: int | None = None
    year: int | None = None

    def __init__(self, data: Tuple[int, int, int]):
        self.id = data[0]
        self.event_id = data[1]
        self.year = data[2]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "date": self.date
        }
    
####################################################################################################

class QuestionType:

    class Type(Enum):
        SINGLE_CHOICE = 1
        MULTI_CHOICE = 2
        INPUT = 3
        INPUT_RANGE = 4

    id: int | None = None
    name: str | None = None

    def __init__(self, data: Tuple[int, str]):
        self.id = data[0]
        self.name = data[1]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
    
####################################################################################################

class Question:

    id: int | None = None
    quiz_id: int | None = None
    type_id: int | None = None
    text: str | None = None

    def __init__(self, data: Tuple[int, int, int, str]):
        match data[2]:
            case "single-choice": type_id = QuestionType.Type.SINGLE_CHOICE.value
            case "multi-choice": type_id = QuestionType.Type.MULTI_CHOICE.value
            case "input": type_id = QuestionType.Type.INPUT.value
            case "input-range": type_id = QuestionType.Type.INPUT_RANGE.value

        self.id = data[0]
        self.quiz_id = data[1]
        self.type_id = type_id
        self.text = data[3]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "type_id": self.type_id,
            "text": self.text
        }

####################################################################################################

class QuestionAnswer:

    id: int | None
    question_id: int | None
    text: str | None = None
    is_correct: bool | None = None

    def __init__(self, data: Tuple[int, int, str, bool]):
        self.id = data[0]
        self.question_id = data[1]
        self.text = data[2]
        self.is_correct = data[3]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "text": self.text,
            "is_correct": self.is_correct
        }


####################################################################################################

class QuestionImage:

    id: int | None = None
    question_id: int | None
    path: str | None = None

    def __init__(self, data: Tuple[int, int, str]):
        self.id = data[0]
        self.question_id = data[1]
        self.path = data[2]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "path": self.path
        }

####################################################################################################

class Solution:

    id: int | None = None
    question_id: int | None
    text: str | None = None

    def __init__(self, data: Tuple[int, int, str]):
        self.id = data[0]
        self.question_id = data[1]
        self.text = data[2]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "text": self.text
        }

####################################################################################################

class SolutionImage:

    id: int | None = None
    solution_id: int | None = None
    path: str | None = None

    def __init__(self, data: Tuple[int, int, str]):
        self.id = data[0]
        self.solution_id = data[1]
        self.path = data[2]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "solution_id": self.solution_id,
            "path": self.path
        }

####################################################################################################

class User:

    id: int | None = None
    email: str | None = None
    username: str | None = None

    def __init__(self, data: Tuple[int, str, str]):
        self.id = data[0]
        self.email = data[1]
        self.username = data[2]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }

####################################################################################################

class UserAnswer:

    id: int | None = None
    user_id: int | None = None
    question_id: int | None = None
    answer_id: int | None = None

    def __init__(self, data: Tuple[int, int, int, int]):
        self.id = data[0]
        self.user_id = data[1]
        self.question_id = data[2]
        self.answer_id = data[3]

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "answer_id": self.answer_id
        }