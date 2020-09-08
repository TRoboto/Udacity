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
        self.database_path = "postgres://postgres:123123@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions_success(self):
        response = self.client().get('/questions')
        data = response.get_json()
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['categories'])
        self.assertEqual(response.status_code, 200)

    def test_get_questions_failed(self):
        response = self.client().get('/questions?page=100')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_delete_questions_success(self):
        response = self.client().delete('/questions/22')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_delete_questions_failed(self):
        response = self.client().delete('/questions/100')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_add_questions_success(self):
        response = self.client().post('/questions',
                                      json={
                                          'question': 'what is my name?',
                                          'answer': 'hq',
                                          'difficulty': 2,
                                          'category': 3,
                                      })
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_get_categories_success(self):
        response = self.client().get('/categories')
        data = response.get_json()
        self.assertTrue(len(data['categories']) > 0)
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_get_categories_failed(self):
        response = self.client().get('/categories/100')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_get_questions_by_category_success(self):
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)

        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertEqual(data['current_category'], 'Geography')

    def test_get_questions_by_category_failed(self):
        response = self.client().get('/categories/12/questions')
        data = json.loads(response.data)

        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_search_questions_success(self):
        response = self.client().post('/questions/search', json={'searchTerm': "the"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(type(data['total_questions']), int)

    def test_search_questions_failed(self):
        response = self.client().post('/questions/search', json={'searchTerm': "tsadashe"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

    def test_get_question_for_quiz_success(self):
        response = self.client().post('/quizzes', json={"previous_questions": [2, 3],
                                                   "quiz_category": {'id': 1, 'type': 'Art'}})
        data = json.loads(response.data)

        self.assertTrue(data['question'])

    def test_get_question_for_quiz_failed(self):
        response = self.client().post('/quizzes', json={"previous_questions": [2, 3],
                                                   "quiz_category": {'id': 9, 'type': 'Science'}})

        self.assertEqual(response.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
