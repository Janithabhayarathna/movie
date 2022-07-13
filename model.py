from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(32))
    released_year = db.Column(db.String(4))
    movie_type = db.Column(db.String(32))

    def __repr__(self):
        return '<Movie %r>' % self.item

    def __init__(self, movie_name, released_year, movie_type):
        self.movie_name = movie_name
        self.released_year = released_year
        self.movie_type = movie_type

