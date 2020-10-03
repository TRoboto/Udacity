from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth.auth import requires_auth, AuthError
from models import setup_db, Actor, Movie

app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app

    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def hello_world():
        return "Hello, World"

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()

        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': list(map(Actor.format, actors))
        }), 200

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()

        if not movies:
            abort(404)

        return jsonify({
            'success': True,
            'movies': list(map(Movie.format, movies))
        }), 200

    # add new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        data = request.get_json()

        if any(x not in data for x in ['name', 'age', 'gender']):
            abort(422)

        actor = Actor(**data)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    # add new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        data = request.get_json()

        if any(x not in data for x in ['title', 'release']):
            abort(422)

        movie = Movie(**data)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    # edit actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, actor_id):
        if not actor_id:
            abort(404)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        data = request.get_json()

        # change name
        if 'name' in data and data['name']:
            actor.name = data['name']

        # change age
        if 'age' in data and data['age']:
            actor.age = data['age']

        # change gender
        if 'gender' in data and data['gender']:
            actor.gender = data['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format(),
        }), 200

    # edit movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        if not movie_id:
            abort(404)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        data = request.get_json()

        # change title
        if 'title' in data and data['title']:
            movie.title = data['title']

        # change release
        if 'release' in data and data['release']:
            movie.release = data['release']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200

    # delete actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        if not actor_id:
            abort(404)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor_id': actor_id
        }), 200

    # delete movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        if not movie_id:
            abort(404)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id
        }), 200

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

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)
