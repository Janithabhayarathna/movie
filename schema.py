from flask_marshmallow import Marshmallow

ma = Marshmallow()


class MovieSchema(ma.Schema):
    class Meta:
        fields = (
            'movie_id',
            'movie_name',
            'released_year',
            'movie_type'
        )


class TheaterSchema(ma.Schema):
    class Meta:
        fields = (
            'theater_id',
            'theater_name',
            'theater_address',
            'theater_type'
        )


class MovieTheaterSchema(ma.Schema):
    class Meta:
        fields = (
            'movie_id',
            'movie_name',
            'released_year',
            'movie_type',
            'theater_id',
            'theater_name',
            'theater_address',
            'theater_type'
        )


class TheaterMovieSchema(ma.Schema):
    class Meta:
        fields = (
            'movie_id',
            'theater_name',
            'theater_address',
            'theater_type'
        )


class ActorSchema(ma.Schema):
    class Meta:
        fields = (
            'actor_id',
            'actor_name',
            'actor_address'
        )


class DirectorSchema(ma.Schema):
    class Meta:
        fields = (
            'director_id',
            'director_name',
            'director_address'
        )
