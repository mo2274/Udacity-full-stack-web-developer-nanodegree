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

db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def Get_Drinks():
    '''
        GET /drinks
            Public endpoint to get all drinks
            returns status code 200
            and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or not found error message
            if there is no drinks
    '''
    try:
        drinks = Drink.query.all()
        drinks = [drink.short() for drink in drinks]
    except:
        abort(422)    

    return jsonify({
        "success": True,
        "drinks": drinks
    })


@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def Get_Drink_Details(payload):
    '''
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
            returns status code 200 and
            json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    try:
        drinks = Drink.query.all()
        drinks = [drink.long() for drink in drinks]
    except:
        abort(422)    

    return jsonify({
        "success": True,
        "drinks": drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def Add_Drink(payload):
    '''
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
            returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''
    body = request.get_json()
    if 'title' not in body or 'recipe' not in body:
        abort(400)
    try:
        title = body.get("title")
        recipe = body.get("recipe")
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
    except BaseException:
        abort(400)
    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def Edit_Drink(payload, id):
    '''
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
            returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        return json.dumps({
            'success': False,
            'error': 'Drink #' + id + ' not found to be edited'
        }), 404    


    body = request.get_json()
    if 'title' not in body and 'recipe' not in body:
        abort(400)
    try:
        title = body.get("title")
        recipe = body.get("recipe")
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        drink = Drink.query.filter(Drink.id == id).one_or_none()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def Delete_Drink(payload, id):
    '''
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
            returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True,
        "delete": id
    })


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def Not_Found(error):
    '''
        Error handler for 404
    '''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


@app.errorhandler(400)
def Bad_Request(error):
    '''
       Error handler for 400
    '''
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(AuthError)
def process_AuthError(error):
    '''
       Error handler for AuthError
    '''
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response
