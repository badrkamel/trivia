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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','Zzz','localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_questions_success(self):
        '''
        tests retrieve paginated questions
        '''

        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_post_new_question(self):
        '''
        tests posting a new question
        '''
        
        response = self.client().post('/questions', json={
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 4,
            'category': 2
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

        self.assertIn('question', data)
        self.assertIn('total_questions', data)
        
        self.assertGreater(data['total_questions'], 0)
        
        self.assertEqual(type(data['total_questions']), int)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()