from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(32))
    released_year = db.Column(db.String(4))
    movie_type = db.Column(db.String(32))
    theater = db.relationship('Theater', backref='Movie')

    def __repr__(self):
        return '<Movie %r>' % self.item

    def __init__(self, movie_name, released_year, movie_type):
        self.movie_name = movie_name
        self.released_year = released_year
        self.movie_type = movie_type


class Theater(db.Model):
    theater_id = db.Column(db.Integer, primary_key=True)
    theater_name = db.Column(db.String(32))
    theater_address = db.Column(db.String(4))
    theater_type = db.Column(db.String(32))

    def __repr__(self):
        return '<Theater %r>' % self.item

    def __init__(self, theater_name, theater_address, theater_type):
        self.theater_name = theater_name
        self.theater_address = theater_address
        self.theater_type = theater_type


# class Actor(db.Model):
#     actor_id = db.Column(db.Integer, primary_key=True)
#     actor_name = db.Column(db.String(32))
#     actor_address = db.Column(db.String(32))
#
#     def __repr__(self):
#         return '<Actor %r>' % self.item
#
#     def __init__(self, actor_name, actor_address):
#         self.actor_name = actor_name
#         self.actor_address = actor_address
#
#
# class Director(db.Model):
#     director_id = db.Column(db.Integer, primary_key=True)
#     director_name = db.Column(db.String(32))
#     director_address = db.Column(db.String(34))
#
#     def __repr__(self):
#         return '<Director %r>' % self.item
#
#     def __init__(self, director_name, director_address):
#         self.director_name = director_name
#         self.director_address = director_address
