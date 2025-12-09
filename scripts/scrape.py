import dotenv
import pathlib
import requests

from src.db.Models import *
from src.db.Database import Database


CWD: str = pathlib.Path(__file__).parent.resolve()
IMG_DIR: str = pathlib.Path.joinpath(CWD, "..", "imgs").resolve()
BASE_URL: str = "https://api.fs-quiz.eu/2"
BASE_IMG_URL: str = "https://img.fs-quiz.eu"

def getEvents() -> list[Event]:
    start_id: int = 1 # server shits the bed when indexing starts at 0
    events: list[Event] = []
    while True:
        response = requests.get(f"{BASE_URL}/event?start_id={start_id}")
        data: list[dict] = response.json()["events"]
        if len(data) == 0: break
        events += [Event((event["id"], event["event_name"])) for event in data]
        if len(data) < 25: break
        start_id = data[-1]["id"] + 1
    return events

def getQuizzes(event_id: int) -> list[Quiz]:
    start_id: int = 1
    quizzes: list[Quiz] = []
    while True:
        response = requests.get(f"{BASE_URL}/quiz?start_id={start_id}&event_id={event_id}&class=ev")
        data: list[dict] = response.json()["quizzes"]
        if len(data) == 0: break
        quizzes += [Quiz((quiz["quiz_id"], event_id, quiz["year"])) for quiz in data]
        if len(data) < 25: break
        start_id = data[-1]["id"] + 1
    return quizzes

def getQuizData(quiz_id: int) -> Tuple[list[Question], list[QuestionAnswer], list[QuestionImage], list[Solution], list[SolutionImage]]:
    questions: list[Question] = []
    answers: list[QuestionAnswer] = []
    question_images: list[QuestionImage] = []
    solutions: list[Solution] = []
    solution_images: list[SolutionImage] = []
    
    response = requests.get(f"{BASE_URL}/quiz/{quiz_id}/questions")
    data: list[dict] = response.json()["questions"]

    for question in data:
        questions.append(Question((question["question_id"], quiz_id, question["type"], question["text"])))
        answers += [QuestionAnswer((answer["answer_id"], answer["question_id"], answer["answer_text"], answer["is_correct"])) for answer in question["answers"]]
        question_images += [QuestionImage((image["img_id"], question["question_id"], image["path"])) for image in question["images"]]

        for solution in question["solution"]:
            solutions.append(Solution((solution["solution_id"], question["question_id"], solution["text"])))
            solution_images += [SolutionImage((image["img_id"], solution["solution_id"], image["path"])) for image in solution["images"]]

    return (questions, answers, question_images, solutions, solution_images)

def saveImage(image: QuestionImage | SolutionImage):
    img_data = requests.get(f"{BASE_IMG_URL}/{image.path}").content
    img_path = pathlib.Path.joinpath(IMG_DIR, image.path)
    output_dir = img_path.parent.resolve()
    if not pathlib.Path.exists(output_dir): pathlib.Path.mkdir(output_dir)
    with open(img_path, "wb") as img_file: img_file.write(img_data)

if __name__ == "__main__":

    dotenv.load_dotenv()
    db: Database = Database()

    events: list[Event] = []
    quizzes: list[Quiz] = []
    questions: list[Question] = []
    question_images: list[QuestionImage] = []
    answers: list[QuestionAnswer] = []
    solutions: list[Solution] = []
    solution_images: list[SolutionImage] = []

    events = getEvents()

    for event in events:
        db.insertEvent(event)
        quizzes += getQuizzes(event.id)

    for quiz in quizzes: 
        db.insertQuiz(quiz)
        q, a, qi, s, si = getQuizData(quiz.id)
        questions += q
        answers += a
        question_images += qi
        solutions += s
        solution_images += si

    for question in questions: db.insertQuestion(question)
    for image in question_images: 
        saveImage(image)
        db.insertQuestionImage(image)
    for answer in answers: db.insertQuestionAnswer(answer)
    for solution in solutions: db.insertQuestionSolution(solution)
    for image in solution_images: 
        saveImage(image)
        db.insertSolutionImage(image)