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
        self.database_path = 'postgresql://mohamed:mohamed@22@localhost:5432/' + self.database_name 
        setup_db(self.app, self.database_path)
        self.new_question = {

        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
   
    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['categories'])) 

    def test_get_paginated_categories_for_errors(self):
        res = self.client().get('/categories?page=1000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 404) 
        self.assertEqual(data['message'], "resource not found")

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['questions'])) 
        self.assertTrue(data['total_questions']) 
        self.assertTrue(len(data['categories'])) 

    def test_get_paginated_questions_for_errors(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 404) 
        self.assertEqual(data['message'], "resource not found")
   
    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['questions'])) 
        self.assertTrue(data['total_questions']) 
        self.assertEqual(data['currentCategory'], 'Art')  
   
    def test_get_category_questions_for_errors(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 404) 
        self.assertEqual(data['message'], "resource not found")
   
    def test_delete_question(self):
        res = self.client().delete('/questions/21')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertEqual(data['deleted'], str(21)) 
   
    def test_delete_question_for_errors(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 422) 
        self.assertEqual(data['message'], "unprocessable")
   
    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': "Tom Hanks"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
        self.assertTrue(len(data['questions'])) 
        self.assertTrue(data['total_questions'])

    def test_search_question_for_errors_emptySearchTerm(self):
        res = self.client().post('/questions', json={'searchTerm': ""})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 422) 
        self.assertEqual(data['message'], "unprocessable")     
    
    def test_add_questions(self):
        res = self.client().post('/questions', json={'question': 'what is your age?', 'answer': '25', 'category': 3, 'difficulty': 1})
        print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 

    def test_add_questions_for_errors_emptyData(self):
        res = self.client().post('/questions', json={})
        print(res)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['error'], 422) 
        self.assertEqual(data['message'], "unprocessable") 
                 
    def test_select_random_question(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'type' : 'Science', 'id' : '1'}, 'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 

    def test_select_random_question_noValidQuestions(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'type': 'Sport', 'id' :'6'}, 'previous_questions': [10, 11]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True) 
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()