from config import db, ma


class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True)
    moviename = db.Column(db.String(32))
    releasedyear = db.Column(db.String(4))
    type = db.Column(db.String(32))


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        sqla_session = db.session
        load_instance = True
