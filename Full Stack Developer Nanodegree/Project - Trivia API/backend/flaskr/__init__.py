import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        all_cat = list(map(Category.format, Category.query.all()))

        if len(all_cat) == 0:
            abort(404)

        output = {'success': True,
                  'categories': all_cat
                  }
        return jsonify(output)

    @app.route('/questions')
    def get_questions():
        ordered_questions = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, ordered_questions)

        if len(questions) == 0:
            abort(404)

        all_cat = list(map(Category.format, Category.query.all()))

        output = {'success': True,
                  'questions': questions,
                  'total_questions': len(ordered_questions),
                  'current_category': None,
                  'categories': all_cat
                  }
        return jsonify(output)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({'success': True,
                            'total_questions': len(Question.query.all())})

        except:
            abort(422)

    @app.route("/questions", methods=['POST'])
    def add_question():
        try:
            question = Question(**request.get_json())
            question.insert()

        except:
            abort(422)

        return jsonify({'success': True,
                        'total_questions': len(Question.query.all())})

    @app.route("/questions/search", methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()

        if len(questions) == 0:
            abort(404)
        try:
            questions = paginate_questions(request, questions)
            all_cat = list(map(Category.format, Category.query.all()))

            output = {'success': True,
                      'questions': questions,
                      'total_questions': len(Question.query.all()),
                      'current_category': None,
                      'categories': all_cat
                      }
            return jsonify(output)
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def get_question_by_category(category_id):
        category = Category.query.get(category_id + 1)
        if category is None:
            abort(404)

        questions = Question.query.filter_by(category=category.id).all()

        if len(questions) == 0:
            abort(404)

        questions = paginate_questions(request, questions)
        all_cat = list(map(Category.format, Category.query.all()))

        output = {'success': True,
                  'questions': questions,
                  'total_questions': len(Question.query.all()),
                  'current_category': category.type,
                  'categories': all_cat
                  }
        return jsonify(output)

    @app.route("/quizzes", methods=['POST'])
    def get_question_for_quiz():
        data = request.get_json()
        if len(data) >= 2:
            id = int(data['quiz_category']['id']) + 1
            prev = data['previous_questions']
            if len(prev) == len(Question.query.filter_by(category=id).all()):
                abort(404)
            elif len(prev) > 0:
                questions = Question.query.filter_by(category=id).filter(~Question.id.in_(prev)).all()
            else:
                questions = Question.query.filter_by(category=id).all()
            if len(questions) == 0:
                abort(404)
            output = {'success': True,
                      'question': Question.format(random.choice(questions))}
            return jsonify(output)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable"
        }), 422

    return app
