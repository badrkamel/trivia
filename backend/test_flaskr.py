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

        self.new_question = {
            "question": "test question",
            "answer": "test answer",
            "difficulty": 4,
            "category": 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that total_questions and questions return data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))


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

    # def test_new_question(self):
    #     '''
    #     tests posting a new question
    #     '''
        
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

    #     self.assertIn('question', data)
        
    #     self.assertGreater(data['total_questions'], 0)
        
    #     self.assertEqual(type(data['total_questions']), int)

        
    def test_delete_question(self):
        """Tests question deletion success"""

        # create a new question to be deleted
        question = Question(
            question=self.new_question['question'], 
            answer=self.new_question['answer'],
            category=self.new_question['category'], 
            difficulty=self.new_question['difficulty']
        )
        question.insert()

        question_id = question.id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        # see if the question has been deleted
        question = Question.query.filter(Question.id == 1).one_or_none()

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if question id matches deleted id
        self.assertEqual(data['deleted'], question_id)

        # check if question equals None after delete
        self.assertEqual(question, None)


    def test_search_questions(self):
        """Tests search questions success"""

        res = self.client().post('/questions',
            json={'searchTerm': 'int'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(len(data['questions']), 2)

        # check that id of question in response is correct
        self.assertEqual(data['questions'][0]['id'], 18)


    # def test_retrieve_questions_by_category(self):
    #     """Tests getting questions by category success"""

    #     res = self.client().get('/categories/1/questions')

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    #     self.assertNotEqual(len(data['questions']), 0)



    def test_play_quiz(self):
        """Tests playing quiz game success"""

        res = self.client().post('/quizzes',
            json={'previous_questions': [18, 21],
               'quiz_category': {'type': 'Art', 'id': '4'}}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # check that the question returned is in correct category
        self.assertEqual(data['question']['category'], '4')

        # check that question returned is not on previous q list
        self.assertNotEqual(data['question']['id'], 18)
        self.assertNotEqual(data['question']['id'], 21)

    def test_play_quiz_fails(self):
        """Tests playing quiz game failure 400"""

        # send post request without json data
        res = self.client().post('/quizzes', json={})

        data = json.loads(res.data)

        # check response status code and message
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()