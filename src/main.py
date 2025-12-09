import json
import flask
import dotenv

from db.Models import *
from db.Database import Database

app: flask.Flask = flask.Flask(__name__)
db: Database | None = None

@app.route("/events", methods=["GET"])
def getEvents():
    events: list[dict] = [event.__dict__() for event in db.getEvents()]
    return app.response_class(
        response=json.dumps({"events": events}),
        status=200,
        mimetype="application/json"
    )

@app.route("/event/<event_id>", methods=["GET"])
def getEvent(event_id: int):
    try: event_id = int(event_id)
    except ValueError: return flask.make_response("Parameter event_id should be an integer", 400)

    event: Event | None = db.getEventById(event_id)
    if event == None: return flask.make_response("Event does not exits", 404)

    return app.response_class(
        response=json.dumps(event.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/quizzes", methods=["GET"])
def getQuizzes():
    quizzes: list[dict] = [quiz.__dict__() for quiz in db.getQuizzes()]
    return app.response_class(
        response=json.dumps({"quizzes": quizzes}),
        status=200,
        mimetype="application/json"
    )

@app.route("/quiz/<quiz_id>", methods=["GET"])
def getQuiz(quiz_id: int):
    try: quiz_id = int(quiz_id)
    except ValueError: return flask.make_response("Parameter quiz_id should be an integer", 400)

    quiz: Quiz | None = db.getQuizById(quiz_id)
    if quiz == None: return flask.make_response("Quiz does not exist", 404)

    return app.response_class(
        response=json.dumps(quiz.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/event_quizzes/<event_id>")
def getEventQuizzes(event_id: int):
    try: event_id = int(event_id)
    except ValueError: return flask.make_response("Parameter event_id should be an integer", 400)

    quizzes: list[dict] = [quiz.__dict__() for quiz in db.getEventQuizzes(event_id)]
    if len(quizzes) == 0: return flask.make_response("Event does not exist", 404)
    return app.response_class(
        response=json.dumps({"quizzes": quizzes}),
        status=200,
        mimetype="application/json"
    )

@app.route("/question_types", methods=["GET"])
def getQuestionTypes():
    question_types: list[dict] = [question_type.__dict__() for question_type in db.getQuestionTypes()]
    return app.response_class(
        response=json.dumps({"question_types": question_types}),
        status=200,
        mimetype="application/json"
    )

@app.route("/question_type/<question_type_id>", methods=["GET"])
def getQuestionType(question_type_id: int):
    try: question_type_id = int(question_type_id)
    except ValueError: return flask.make_response("Parameter question_type_id should be an integer", 400)

    question_type: QuestionType | None = db.getQuestionTypeById(question_type_id)
    if question_type == None: return flask.make_response("Question type does not exist", 404)

    return app.response_class(
        response=json.dumps(question_type.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/questions", methods=["GET"])
def getQuestions():
    questions: list[dict] = [question.__dict__() for question in db.getQuestions()]
    return app.response_class(
        response=json.dumps({"questions": questions}),
        status=200,
        mimetype="application/json"
    )

@app.route("/question/<question_id>", methods=["GET"])
def getQuestion(question_id: int):
    try: question_id = int(question_id)
    except ValueError: return flask.make_response("Parameter question_id should be an integer", 400)

    question: Question | None = db.getQuestionById(question_id)
    if question == None: return flask.make_response("Question does not exist", 404)

    return app.response_class(
        response=json.dumps(question.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/quiz_questions/<quiz_id>", methods=["GET"])
def getQuizQuestions(quiz_id: int):
    try: quiz_id = int(quiz_id)
    except ValueError: return flask.make_response("Parameter quiz_id should be an integer", 400)

    questions: list[dict] = [question.__dict__() for question in db.getQuizQuestions(quiz_id)]
    if len(questions) == 0: return flask.make_response("Quiz does not exist", 404)
    return app.response_class(
        response=json.dumps({"questions": questions}),
        status=200,
        mimetype="application/json"
    )

@app.route("/question_answers/<question_id>", methods=["GET"])
def getQuestionAnswers(question_id: int):
    try: question_id = int(question_id)
    except ValueError: return flask.make_response("Parameter question_id should be an integer", 400)

    answers: list[dict] = [answer.__dict__() for answer in db.getQuestionAnswers(question_id)]
    if len(answers) == 0: return flask.make_response("Question does not exist", 404)
    return app.response_class(
        response=json.dumps({"answers": answers}),
        status=200,
        mimetype="application/json"
    )

@app.route("/answers/<answer_id>", methods=["GET"])
def getQuestionAnswer(answer_id: int):
    try: answer_id = int(answer_id)
    except ValueError: return flask.make_response("Parameter answer_id should be an integer", 400)

    answer: QuestionAnswer | None = db.getQuestionAnswerById(answer_id)
    if answer == None: return flask.make_response("Answer does not exist", 404)

    return app.response_class(
        response=json.dumps(answer.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/question_images/<question_id>", methods=["GET"])
def getQuestionImages(question_id: int):
    try: question_id = int(question_id)
    except ValueError: return flask.make_response("Parameter question_id should be an integer", 400)

    images: list[dict] = [image.__dict__() for image in db.getQuestionImages(question_id)]
    return app.response_class(
        response=json.dumps({"images": images}),
        status=200,
        mimetype="application/json"
    )

@app.route("/question_image/<image_id>", methods=["GET"])
def getQuestionImage(image_id: int):
    try: image_id = int(image_id)
    except ValueError: return flask.make_response("Parameter image_id should be an integer", 400)

    image: QuestionImage | None = db.getQuestionImageById(image_id)
    if image == None: return flask.make_response("Image does not exist", 404)

    return app.response_class(
        response=json.dumps(image.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/solutions/<question_id>", methods=["GET"])
def getSolutions(question_id: int):
    try: question_id = int(question_id)
    except ValueError: return flask.make_response("Parameter question_id should be an integer", 400)

    solutions: list[dict] = [solution.__dict__() for solution in db.getQuestionSolutions(question_id)]
    return app.response_class(
        response=json.dumps({"solutions": solutions}),
        status=200,
        mimetype="application/json"
    )

@app.route("/solution/<solution_id>", methods=["GET"])
def getSolution(solution_id: int):
    try: solution_id = int(solution_id)
    except ValueError: return flask.make_response("Parameter solution_id should be an integer", 400)

    solution: Solution | None = db.getQuestionSolutionById(solution_id)
    if solution == None: return flask.make_response("Solution does not exist", 404)

    return app.response_class(
        response=json.dumps(solution.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/solution_images/<solution_id>", methods=["GET"])
def getSolutionImages(solution_id: int):
    try: solution_id = int(solution_id)
    except ValueError: return flask.make_response("Parameter solution_id should be an integer", 400)

    images: list[dict] = db.getSolutionImages(solution_id)
    return app.response_class(
        response=json.dumps({"images": images}),
        status=200,
        mimetype="application/json"
    )

@app.route("/solution_image/<image_id>", methods=["GET"])
def getSolutionImage(image_id: int):
    try: image_id = int(image_id)
    except ValueError: return flask.make_response("Parameter image_id should be an integer", 400)

    image: SolutionImage | None = db.getSolutionImageById(image_id)
    if image == None: return flask.make_response("Image does not exist", 404)

    return app.response_class(
        response=json.dumps(image.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/users", methods=["GET"])
def getUsers():
    users: list[dict] = [user.__dict__() for user in db.getUsers()]
    return app.response_class(
        response=json.dumps({"users": users}),
        status=200,
        mimetype="application/json"
    )

@app.route("/user_by_id/<user_id>", methods=["GET"])
def getUserById(user_id: int):
    try: user_id = int(user_id)
    except ValueError: return flask.make_response("Parameter user_id should be an integer", 400)

    user: User | None = db.getUserById(user_id)
    if user == None: return flask.make_response("User does not exist", 404)

    return app.response_class(
        response=json.dumps(user.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/user_by_email/<user_email>", methods=["GET"])
def getUserByEmail(user_email: str):
    user: User | None = db.getUserByEmail(user_email)
    if user == None: return flask.make_response("User does not exist", 404)

    return app.response_class(
        response=json.dumps(user.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/user_by_username/<username>", methods=["GET"])
def getUserByUsername(username: str):
    user: User | None = db.getUserByUsername(username)
    if user == None: return flask.make_response("User does not exist", 404)

    return app.response_class(
        response=json.dumps(user.__dict__()),
        status=200,
        mimetype="application/json"
    )

@app.route("/users_answers", methods=["GET"])
def getUsersAnswers():
    answers: list[dict] = [answer.__dict__() for answer in db.getUsersAnswers()]
    return app.response_class(
        response=json.dumps({"answers": answers}),
        status=200,
        mimetype="application/json"
    )

@app.route("/user_answers/<user_id>", methods=["GEt"])
def getUserAnswers(user_id: int):
    try: user_id = int(user_id)
    except ValueError: return flask.make_response("Parameter user_id should be an integer", 400)

    answers: list[dict] = [answer.__dict__() for answer in db.getUserAnswers(user_id)]
    return app.response_class(
        response=json.dumps({"answers": answers}),
        status=200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    dotenv.load_dotenv()
    db = Database()
    app.run(host="0.0.0.0", port=5000, debug=False)