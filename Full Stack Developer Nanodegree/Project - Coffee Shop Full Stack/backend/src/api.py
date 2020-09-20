import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()


## ROUTES

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': list(map(Drink.short, drinks))
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': list(map(Drink.long, drinks))
    }), 200


@app.route("/drinks", methods=['POST'])
@requires_auth("post:drinks")
def create_drink(payload):
    if request.data:
        data = json.loads(request.data.decode('utf-8'))
        new_drink = Drink(title=data['title'], recipe=json.dumps(data['recipe']))
        Drink.insert(new_drink)
        drinks = list(map(Drink.long, Drink.query.all()))
        return jsonify({
            "success": True,
            "drinks": drinks
        })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    data = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        if data.get('title'):
            drink.title = data.get('title')

        if data.get('recipe'):
            drink.recipe = json.dumps(data['recipe'])

        drink.update()

    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]}), 200


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except:
        abort(400)

    return jsonify({'success': True, 'delete': drink_id}), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
