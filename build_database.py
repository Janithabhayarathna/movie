import os
from config import db
from models import Movie

MOVIE = [
    {"moviename": "Zoom", "releasedyear": "2022", "type": "Action"},
    {'moviename': 'Beast', 'releasedyear': '2022', 'type': 'Crime'},
    {'moviename': 'Don', 'releasedyear': '2022', 'type': 'Drama'},
    {'moviename': 'Major', 'releasedyear': '2022', 'type': 'Action'},
    {'moviename': 'Inceptor', 'releasedyear': '2022', 'type': 'Adventure'}
]

if os.path.exists('movie.db'):
    os.remove('movie.db')

db.create_all()

for movie in MOVIE:
    m = Movie(moviename=movie.get("moviename"), releasedyear=movie.get("releasedyear"), type=movie.get("type"))
    db.session.add(m)

db.session.commit()
