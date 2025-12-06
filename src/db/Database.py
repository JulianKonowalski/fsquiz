import os
import psycopg2

from db.Models import *

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

    def getEvents(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events;")
        results = cursor.fetchall()
        cursor.close()
        return [Event(result).__dict__() for result in results]

    ################################################################################################

    def getEventById(self, event_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM events e WHERE e.id={event_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return Event(result).__dict__()
    
    ################################################################################################

    def insertEvent(self, event_name: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO events (name) 
                VALUES ('{event_name}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    
    ################################################################################################

    def getQuizzes(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM quizzes;")
        results = cursor.fetchall()
        cursor.close()
        return [Quiz(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuizById(self, quiz_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM quizzes q WHERE q.id={quiz_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return Quiz(result).__dict__()
    
    ################################################################################################

    def getEventQuizzes(self, event_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM quizzes q WHERE q.event_id={event_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Quiz(result).__dict__() for result in results]
    
    ################################################################################################

    def insertQuiz(self, event_id: int, year: int) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO quizzes (event_id, year) 
                VALUES ({event_id}, {year}) 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getQuestionTypes(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM question_types;")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionType(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuestionTypeById(self, question_type_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_types t WHERE t.id={question_type_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return QuestionType(result).__dict__()
    
    ################################################################################################

    def getQuestions(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM questions;")
        results = cursor.fetchall()
        cursor.close()
        return [Question(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuestionById(self, question_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM questions q WHERE q.id={question_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return Question(result).__dict__()
    
    ################################################################################################

    def getQuizQuestions(self, quiz_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM questions q WHERE q.quiz_id={quiz_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Question(result).__dict__() for result in results]
    
    ################################################################################################

    def insertQuestion(self, quiz_id: int, type_id: int, text: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO questions (quiz_id, type_id, text) 
                VALUES ({quiz_id}, {type_id}, '{text}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getQuestionAnswers(self, question_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_answers a WHERE a.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionAnswer(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuestionAnswerById(self, question_answer_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_answers a WHERE a.id={question_answer_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return QuestionAnswer(result).__dict__() 
    
    ################################################################################################

    def insertQuestionAnswer(self, question_id: int, text: str, is_correct: bool) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            is_correct: str = "true" if is_correct else "false"
            cursor.execute(f"""
                INSERT INTO question_answers (question_id, text, is_correct)
                VALUES ({question_id}, '{text}', {is_correct}) 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    ################################################################################################

    def getQuestionImages(self, question_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_images i WHERE i.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [QuestionImage(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuestionImageById(self, question_image_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM question_images i WHERE i.id={question_image_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return QuestionImage(result).__dict__()
    
    ################################################################################################

    def insertQuestionImage(self, question_id: int, path: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO question_images (question_id, path)
                VALUES ({question_id}, '{path}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result

    ################################################################################################

    def getQuestionSolutions(self, question_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solutions s WHERE s.question_id={question_id};")
        results = cursor.fetchall()
        cursor.close()
        return [Solution(result).__dict__() for result in results]
    
    ################################################################################################

    def getQuestionSolutionById(self, question_solution_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solutions s WHERE s.question_id={question_solution_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return Solution(result).__dict__()
    
    ################################################################################################

    def insertQuestionSolution(self, question_id: int, text: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO solutions (question_id, text)
                VALUES ({question_id}, '{text}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getSolutionImages(self, solution_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solution_images i WHERE i.solution_id={solution_id};")
        results = cursor.fetchall()
        cursor.close()
        return [SolutionImage(result).__dict__() for result in results]
    
    ################################################################################################

    def getSolutionImageById(self, solution_image_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM solution_images i WHERE i.id={solution_image_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return SolutionImage(result).__dict__()
    
    ################################################################################################

    def insertSolutinoImage(self, solution_id: int, path: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO solution_images (solution_id, path)
                VALUES ({solution_id}, '{path}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getUsers(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        cursor.close()
        return [User(result).__dict__() for result in results]
    
    ################################################################################################

    def getUserById(self, user_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.id={user_id};")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return User(result).__dict__()
    
    ################################################################################################

    def getUserByEmail(self, user_email: str) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.email='{user_email}';")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return User(result).__dict__()       
    
    ################################################################################################

    def getUserByUsername(self, username: str) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM users u WHERE u.username='{username}';")
        result = cursor.fetchall()
        cursor.close()
        if not result: return None
        else: return User(result).__dict__()       
    
    ################################################################################################

    def insertUser(self, user_email: str, username: str) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO users (email, username)
                VALUES ('{user_email}', '{username}') 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result
    
    ################################################################################################

    def getUsersAnswers(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_answers;")
        results = cursor.fetchall()
        cursor.close()
        return [UserAnswer(result).__dict__() for result in results]
    
    ################################################################################################

    def getUserAnswers(self, user_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM user_answers a WHERE a.user_id={user_id};")
        results = cursor.fetchall()
        cursor.close()
        return [UserAnswer(result).__dict__() for result in results]     
    
    ################################################################################################

    def createUserAnswer(self, user_id: int, question_id: int, answer_id: int) -> int | None:
        result: int | None = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO user_answers (user_id, question_id, answer_id)
                VALUES ({user_id}, {question_id}, {answer_id}) 
                RETURNING id;
            """)
            result = cursor.fetchone()[0]
            self.connection.commit()
        except: self.connection.rollback()
        cursor.close()
        return result       