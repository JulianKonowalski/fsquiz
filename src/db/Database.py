import os
import psycopg2

from .Models import * 

class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_HOST_PORT")
        )

    ################################################################################################

    def getEvents(self) -> list[Event]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events;")
        results = cursor.fetchall()
        cursor.close()
        return [Event(result) for result in results]

    ################################################################################################

    def getEventById(self, event_id: int) -> Event | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM events e WHERE e.id={event_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return Event(result)
    
    ################################################################################################

    def insertEvent(self, event: Event) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO events (id, name) 
                VALUES ({event.id}, '{event.name}');
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    
    ################################################################################################

    def getQuizzes(self) -> list[Quiz]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM quizzes;")
        results = cursor.fetchall()
        cursor.close()
        return [Quiz(result) for result in results]
    
    ################################################################################################

    def getQuizById(self, quiz_id: int) -> Quiz | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM quizzes q WHERE q.id={quiz_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return Quiz(result)
    
    ################################################################################################

    def getEventQuizzes(self, event_id: int) -> list[Quiz]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM quizzes q WHERE q.event_id={event_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Quiz(result) for result in results]
    
    ################################################################################################

    def insertQuiz(self, quiz: Quiz) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO quizzes (id, event_id, year) 
                VALUES ({quiz.id}, {quiz.event_id}, {quiz.year});
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getQuestionTypes(self) -> list[QuestionType]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM question_types;")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionType(result) for result in results]
    
    ################################################################################################

    def getQuestionTypeById(self, question_type_id: int) -> QuestionType | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_types t WHERE t.id={question_type_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return QuestionType(result)
    
    ################################################################################################

    def getQuestions(self) -> list[Question]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM questions;")
        results = cursor.fetchall()
        cursor.close()
        return [Question(result) for result in results]
    
    ################################################################################################

    def getQuestionById(self, question_id: int) -> Question | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM questions q WHERE q.id={question_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return Question(result)
    
    ################################################################################################

    def getQuizQuestions(self, quiz_id: int) -> list[Question]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM questions q WHERE q.quiz_id={quiz_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Question(result) for result in results]
    
    ################################################################################################

    def insertQuestion(self, question: Question) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO questions (id, quiz_id, type_id, text) 
                VALUES ({question.id}, {question.quiz_id}, {question.type_id}, '{question.text}');
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getQuestionAnswers(self, question_id: int) -> list[QuestionAnswer]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_answers a WHERE a.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionAnswer(result) for result in results]
    
    ################################################################################################

    def getQuestionAnswerById(self, question_answer_id: int) -> QuestionAnswer | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_answers a WHERE a.id={question_answer_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return QuestionAnswer(result)
    
    ################################################################################################

    def insertQuestionAnswer(self, answer: QuestionAnswer) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            is_correct: str = "true" if answer.is_correct else "false"
            cursor.execute(f"""
                INSERT INTO question_answers (id, question_id, text, is_correct)
                VALUES ({answer.id}, {answer.question_id}, '{answer.text}', {is_correct});
            """)
            result = True 
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    ################################################################################################

    def getQuestionImages(self, question_id: int) -> list[QuestionImage]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_images i WHERE i.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionImage(result) for result in results]
    
    ################################################################################################

    def getQuestionImageById(self, question_image_id: int) -> QuestionImage | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_images i WHERE i.id={question_image_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return QuestionImage(result)
    
    ################################################################################################

    def insertQuestionImage(self, image: QuestionImage) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO question_images (id, question_id, path)
                VALUES ({image.id}, {image.question_id}, '{image.path}');
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    ################################################################################################

    def getQuestionSolutions(self, question_id: int) -> list[Solution]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solutions s WHERE s.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Solution(result) for result in results]
    
    ################################################################################################

    def getQuestionSolutionById(self, question_solution_id: int) -> Solution | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solutions s WHERE s.question_id={question_solution_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return Solution(result)
    
    ################################################################################################

    def insertQuestionSolution(self, solution: Solution) -> bool:
        result: bool = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO solutions (id, question_id, text)
                VALUES ({solution.id}, {solution.question_id}, '{solution.text}');
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getSolutionImages(self, solution_id: int) -> list[SolutionImage]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solution_images i WHERE i.solution_id={solution_id};")
        results = cursor.fetchall()
        cursor.close()
        return [SolutionImage(result) for result in results]
    
    ################################################################################################

    def getSolutionImageById(self, solution_image_id: int) -> SolutionImage | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solution_images i WHERE i.id={solution_image_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return SolutionImage(result)
    
    ################################################################################################

    def insertSolutionImage(self, image: SolutionImage) -> bool:
        result: bool = False 
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO solution_images (id, solution_id, path)
                VALUES ({image.id}, {image.solution_id}, '{image.path}');
            """)
            result = True
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getUsers(self) -> list[User]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        cursor.close()
        return [User(result) for result in results]
    
    ################################################################################################

    def getUserById(self, user_id: int) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.id={user_id};")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return User(result)
    
    ################################################################################################

    def getUserByEmail(self, user_email: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.email='{user_email}';")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return User(result)

    ################################################################################################

    def getUserByUsername(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.username='{username}';")
        result = cursor.fetchone()
        cursor.close()
        if not result: return None
        else: return User(result)

    ################################################################################################

    def insertUser(self, user: User) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO users (email, username)
                VALUES ('{user.email}', '{user.username}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getUsersAnswers(self) -> list[UserAnswer]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_answers;")
        results = cursor.fetchall()
        cursor.close()
        return [UserAnswer(result) for result in results]
    
    ################################################################################################

    def getUserAnswers(self, user_id: int) -> list[UserAnswer]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM user_answers a WHERE a.user_id={user_id};")
        results = cursor.fetchall()
        cursor.close()
        return [UserAnswer(result) for result in results]     
    
    ################################################################################################

    def createUserAnswer(self, answer: UserAnswer) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO user_answers (user_id, question_id, answer_id)
                VALUES ({answer.user_id}, {answer.question_id}, {answer.answer_id})
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result       