import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "root", "localhost:5432", self.database_name
        )
        
        setup_db(self.app, self.database_path)
        self.new_question = {"question": "The moon is...", "answer": "yellow", "difficulty": 2, "category":2}
        self.new_question_two = {"question": None, "answer": None, "difficulty": None, "category":None}
        self.quiz_request = {"previous_questions": [31], "quiz_category": {"type": "Geography", "id": 3} }
        self.quiz_request_two = {"previous_questions": [30,31], "quiz_category": {"type": "Geography", "id": 3} }
        self.quiz_request_without_category = {"previous_questions": [30,31], "quiz_category": {"type": "click", "id": 0} }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    # def test_404_for_categories(self):
    #     res = self.client().get("/categories")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/1')
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertEqual(question, None)

    def test_404_if_book_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        pass

    def test_422_if_question_creation_fails(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        pass
    
    def test_422_if_question_has_missing_values(self):
        res = self.client().post("/questions", json=self.new_question_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
    
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "Zambia"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_questions_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "blackjacks"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])

    def test_get_next_question_in_quiz(self):
        res = self.client().post("/quizzes", json=self.quiz_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertFalse(data["question"]["id"] in self.quiz_request["previous_questions"])
   
    def test_get_next_question_in_quiz_without_category(self):
        res = self.client().post("/quizzes", json=self.quiz_request_without_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertFalse(data["question"]["id"] in self.quiz_request["previous_questions"])
   
    def test_get_next_question_in_quiz_if_all_questions_are_done(self):
        res = self.client().post("/quizzes", json=self.quiz_request_two)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"] == None)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()