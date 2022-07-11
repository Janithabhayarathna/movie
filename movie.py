from flask import make_response, abort
from config import db
from models import Movie, MovieSchema


def create(movie):
    moviename = movie.get("moviename", None)
    releasedyear = movie.get("releasedyear", None)
    type = movie.get("type", None)

    existing_movie = (
        Movie.query.filter(Movie.moviename == moviename)
        .filter(Movie.releasedyear == releasedyear)
        .filter(Movie.type == type)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_movie is None:

        # Create a person instance using the schema and the passed in person
        schema = MovieSchema()
        new_movie = schema.load(movie, session=db.session).data

        # Add the person to the database
        db.session.add(new_movie)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_movie)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "movie {moviename} exists already".format(
                moviename=moviename
            ),
        )


def read():
    movie = Movie.query.order_by(Movie.moviename).all()
    movie_schema = MovieSchema(many=True)
    return movie_schema.dump(movie).data


def read_one(movie_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
    if movie is not None:
        movie_schema = MovieSchema()
        return movie_schema.dump(movie).data
    else:
        abort(
            404, "Movie id {movienameone} not found".format(movienameone=movie_id)
        )

    return movie


def update(movie_id, movie):
    # Get the person requested from the db into session
    update_movie = Movie.query.filter(
        Movie.movie_id == movie_id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    moviename = movie.get("moviename")
    releasedyear = movie.get("releasedyear")
    type = movie.get("type")

    existing_movie = (
        Movie.query.filter(Movie.moviename == moviename)
        .filter(Movie.releasedyear == releasedyear)
        .filter(Movie.type == type)
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
            "Movie {moviename} exists already".format(
                moviename=moviename
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id to the person we want to update
        update.movie_id = update_movie.movie_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_movie)

        return data, 200
