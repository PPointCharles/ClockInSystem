from database import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, user_id, time):
        self.user_id = user_id
        self.time = time


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    duration = db.Column(db.Float)

    def __init__(self, user_id, year, month, day, duration):
        self.user_id = user_id
        self.year = year
        self.month = month
        self.day = day
        self.duration = duration


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password
