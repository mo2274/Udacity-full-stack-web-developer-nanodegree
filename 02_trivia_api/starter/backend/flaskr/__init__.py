import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formated_items = [category.format() for category in selection]
    return formated_items[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        '''
            This method is responsable for,
            adding the allowed headers and allowed methods.

            @args : response
            @return : the response with new modifications
        '''
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        '''
          This endpoint is resposable for,
          handling GET requests for categories path.

          @return  : all available categories and a success message.
        '''
        selection = Category.query.order_by(Category.id).all()
        paginated_categories = paginate_items(request, selection)
        categoreis = {category['id']: category['type'] for category in paginated_categories}

        if len(categoreis) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categoreis
        })

    @app.route('/questions')
    def get_quastions():
        '''
            This endpoint is responsable for,
            handling GET requests for questions,
            including pagination (every 10 questions).

            @return : This endpoint should return,
            a list of paginated questions (page 1 as default),
            number of total questions, current category, categories.
        '''
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_items(request, questions)

        categoreis = Category.query.order_by(Category.id).all()
        current_categoreis = {
            category.id: category.type for category in categoreis}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': current_categoreis,
            'current_category': 'sport'
        })

    @app.route('/categories/<category_id>/questions')
    def get_category_questions(category_id):
        '''
            This endpoint is responsable for,
            getting the questions related to a specific category,

            @return : This endpoint should return a list of questions,
            number of total questions, current category.
        '''
        current_category = Category.query.filter(
            Category.id == category_id).one_or_none()
        questions = Question.query.filter(
            Question.category == category_id).order_by(
            Question.id).all()
        current_questions = paginate_items(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'currentCategory': current_category.type
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        Endpoint to DELETE question using a question ID.

        @return : json object includes the deleted question id
        '''
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        '''
          Endpoint to POST a new question OR search for a specific question.

          @return : This endpoint should return a list of questions,
          number of total questions, current category.
        '''
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            if body.get('searchTerm'):
                result_questions = Question.query.filter(
                    Question.question.ilike(
                        '%{}%'.format(
                            body.get('searchTerm')))).all()
                questions = [Q.format() for Q in result_questions]
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(questions)
                })

            else:
                if question is None or answer is None:
                    abort(422)
                if question == "" or answer == "":
                    abort(422)
                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)
                question.insert()
                return jsonify({
                    'success': True
                })

        except BaseException:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def select_random_question():
        '''
          This endpoint to get questions to play the quiz,
          the endpoint should take category and,
          previous question parameters from the request body.

          @return : if there is a valid question it will return,
          the formated question with success message,
          and if no valid questions it will return,
          just the messege with no questions.
        '''
        try:
            body = request.get_json()
            category = body.get('quiz_category')['id']
            previous_questions = body.get('previous_questions')
            if category:
                questions = Question.query.filter(
                    Question.category == category).all()
            else:
                questions = Question.query.all()
            questions_ids = [q.id for q in questions]
            valid_questions = list(
                set(previous_questions) ^ set(questions_ids))
            if len(valid_questions) == 0:
                return jsonify({
                    'success': True
                })
            n = random.randint(0, len(valid_questions) - 1)
            selected_question_id = valid_questions[n]
            question = Question.query.filter(
                Question.id == selected_question_id).one_or_none()
        except BaseException:
            abort(422)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        '''
          Error handler for the 404 Error

          @return : a message indicates that the resource is not found
        '''
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        '''
          Error handler for the 422 Error

          @return : a message indicates that the request is unprocessable
        '''
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        '''
          Error handler for the 400 Error

          @return : a message indicates that the request is a bad request
        '''
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400    

    return app
