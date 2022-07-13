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
    update_movie = Movie.query.filter(
        Movie.movie_id == movie_id
    ).first()

    # Try to find an existing movie with the same name as the update
    movie_name = movie.get("movie_name")
    released_year = movie.get("released_year")
    movie_type = movie.get("movie_type")

    existing_movie = (
        Movie.query.filter(Movie.movie_name == movie_name)
        .filter(Movie.released_year == released_year)
        .filter(Movie.movie_type == movie_type)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_movie is None:
        abort(
            404,
            "Movie not found for Id: {movie_id}".format(movie_id=movie_id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
            existing_movie is not None and existing_movie.movie_id != movie_id
    ):
        abort(
            409,
            "Movie {movie_name} exists already".format(
                movie_name=movie_name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in movie into a db object
        schema = MovieSchema()
        update = schema.load(movie)
        movie_schema = MovieSchema()
        data_existing = movie_schema.jsonify(update_movie)
        data_new = movie_schema.jsonify(update)
        # Set the id to the movie we want to update
        data_new.movie_id = data_existing.movie_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data_existing = schema.dump(update_movie)

        return data_existing, 200


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
