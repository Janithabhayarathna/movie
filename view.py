from model import Movie, db
from schema import MovieSchema
from flask import Flask, jsonify, request, abort


def get(movie_id=None):

    try:
        if movie_id is None:
            movie = Movie.query.filter().all()
            movie_schema = MovieSchema(many=True)
            return movie_schema.jsonify(movie)
        else:
            movie = Movie.query.filter_by(movie_id=movie_id).first()
            movie_schema = MovieSchema()
            return movie_schema.jsonify(movie)

    except Exception as e:
        jsonify({"error": "There was an error."})

# def get_one(movie_id=None):
#
#     try:
#         if movie_id is not None:
#             movie = Movie.query.filter().all()
#             movie_schema = MovieSchema()
#             return movie_schema.jsonify(movie)
#         else:
#             abort(
#                 404, "Not found"
#             )
#
#     except Exception as e:
#         jsonify({"error": "There was an error."})


def post():

    data = request.get_json()
    try:
        new_movie = Movie(**data)
        movie_schema = MovieSchema()
        db.session.add(new_movie)
        db.session.commit()
        return movie_schema.jsonify(new_movie)

    except Exception as e:
        print(e)
        jsonify({"error": "There was an error."})


def put(movie_id):

    try:
        data = request.get_json()
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        movie = Movie.query.filter_by(movie_id=movie_id)
        movie.update(data)
        db.session.commit()

        return jsonify(data)

    except Exception as e:
        jsonify({"error": "There was an error"})  # Routes
