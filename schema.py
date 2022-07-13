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
