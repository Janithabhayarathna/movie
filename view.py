from model import Movie, Theater, db
from schema import MovieSchema, TheaterSchema, TheaterMovieSchema, MovieTheaterSchema
from flask import jsonify, request, abort, make_response


def get_movie_list(movie_id=None):
    year = request.args.get("year", type=str)
    try:

        if year is not None:
            movie = Movie.query.filter_by(released_year=year).all()
            movie_schema = MovieSchema(many=True)
            return movie_schema.jsonify(movie)

        elif movie_id is None:
            movie = Movie.query.filter().all()
            movie_schema = MovieSchema(many=True)
            return movie_schema.jsonify(movie)

        else:
            movie = Movie.query.filter_by(movie_id=movie_id).first()
            movie_schema = MovieSchema()
            return movie_schema.jsonify(movie)

    except Exception as e:
        jsonify({"error": "There was an error."})


def get_one_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).outerjoin(Theater).one_or_none()
    if movie is not None:
        movie_schema = MovieTheaterSchema()
        return movie_schema.jsonify(movie)
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def post_movie():
    data = request.get_json()
    try:
        new_movie = Movie(**data)
        movie_schema = MovieTheaterSchema()
        db.session.add(new_movie)

        db.session.commit()
        return movie_schema.jsonify(new_movie)

    except Exception as e:
        print(e)
        jsonify({"error": "There was an error."})


def update_movie(movie_id):
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
        new_movie.movie_id = movie_id

        schema = MovieTheaterSchema()

        db.session.merge(new_movie)
        db.session.commit()

        movie_data = schema.dump(existing_movie)

        return movie_data, 200


def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted successfully".format(movie_id=movie_id), 200
        )

    else:
        abort(
            404,
            "Movie not found for Id: {movie_id}".format(movie_id=movie_id),
        )


def get_theater_list(theater_id=None):
    try:
        if theater_id is None:
            theater = Theater.query.filter().all()
            theater_schema = TheaterSchema(many=True)
            return theater_schema.jsonify(theater)

        else:
            theater = Movie.query.filter_by(theater_id=theater_id).first()
            theater_schema = TheaterSchema()
            return theater_schema.jsonify(theater)

    except Exception as e:
        jsonify({"error": "An error occurred."})


def get_one_theater(theater_id):
    theater = Theater.query.filter_by(theater_id=theater_id).first()
    theater_schema = TheaterSchema()
    return theater_schema.jsonify(theater)


# def get_one_theater_movie(movie_id, theater_id):
#     theater = Theater.query.join(Movie, Movie.movie_id == Theater.theater_id).filter(Movie.movie_id == movie_id).filter(Theater.theater_id == theater_id).one_or_none()
#     if theater is not None:
#         theater_schema = TheaterSchema()
#         data = theater_schema.dump(theater).data
#         return data
#
#     else:
#         abort(404, f"Theater not found for Id: {theater_id}")
#
#     theater_schema = TheaterSchema()
#     return theater_schema.jsonify(theater)


def post_theater():
    data = request.get_json()
    try:
        new_theater = Theater(**data)
        theater_schema = TheaterSchema()
        db.session.add(new_theater)

        db.session.commit()
        return theater_schema.jsonify(new_theater)

    except Exception as e:
        print(e)
        jsonify({"error": "There was an error."})


def post_theater_movie(movie_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
    data = request.get_json()

    theater_name = data.get("theater_name")
    theater_address = data.get("theater_address")
    theater_type = data.get("theater_type")

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    else:

        new_theater = Theater(theater_name, theater_address, theater_type)
        new_theater.movie_id = movie_id

        schema = TheaterMovieSchema()

        db.session.merge(new_theater)
        db.session.commit()

        theater_data = schema.dump(new_theater)

        return theater_data, 200


def update_theater(theater_id):
    theater = request.get_json()
    existing_theater = Theater.query.filter(
        Theater.theater_id == theater_id
    ).one_or_none()

    theater_name = theater.get("theater_name")
    theater_address = theater.get("theater_address")
    theater_type = theater.get("theater_type")

    if existing_theater is None:
        abort(
            404,
            "Theater not found for Id: {theater_id}".format(theater_id=theater_id),
        )

    else:

        new_theater = Theater(theater_name, theater_address, theater_type)
        new_theater.theater_id = theater_id

        schema = TheaterSchema()

        db.session.merge(new_theater)
        db.session.commit()

        theater_data = schema.dump(existing_theater)

        return theater_data, 200


def delete_theater(theater_id):
    theater = Theater.query.filter(Theater.theater_id == theater_id).one_or_none()

    if theater is not None:
        db.session.delete(theater)
        db.session.commit()
        return make_response(
            "Theater {theater_id} deleted successfully".format(theater_id=theater_id), 200
        )

    else:
        abort(
            404,
            "Theater not found for Id: {theater_id}".format(theater_id=theater_id),
        )
