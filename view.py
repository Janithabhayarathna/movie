from model import Movie, db
from schema import MovieSchema
from flask import jsonify, request, abort, make_response


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


def get_one(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    movie_schema = MovieSchema()
    return movie_schema.jsonify(movie)


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


def update(movie_id):
    movie = request.get_json()
    existing_movie = Movie.query.filter(
        Movie.movie_id == movie_id
    ).one_or_none()

    movie_name = movie.get("movie_name")
    released_year = movie.get("released_year")
    movie_type = movie.get("movie_type")

    if existing_movie is None:
        abort(
            404,
            "Movie not found for Id: {movie_id}".format(movie_id=movie_id),
        )

    else:

        new_movie = Movie(movie_name, released_year, movie_type)

        schema = MovieSchema()

        new_movie.movie_id = movie_id

        db.session.merge(new_movie)
        db.session.commit()

        movie_data = schema.dump(existing_movie)

        return movie_data, 200


def delete(movie_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted".format(movie_id=movie_id), 200
        )

    else:
        abort(
            404,
            "Movie not found for Id: {movie_id}".format(movie_id=movie_id),
        )
