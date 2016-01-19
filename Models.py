from Database import db

import datetime


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False)
    subject = db.Column(db.String(), unique=False)
    body = db.Column(db.String(), unique=False)
    views = db.Column(db.Integer, unique=False)

    def __init__(self, subject, body):
        self.timestamp = datetime.datetime.now()
        self.subject = subject
        self.body = body
        self.views = 0


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False)
    question_id = db.Column(db.Integer, unique=False)
    body = db.Column(db.String(), unique=False)
    upvote_count = db.Column(db.Integer, unique=False)

    def __init__(self, question_id, body):
        self.timestamp = datetime.datetime.now()
        self.question_id = question_id
        self.body = body
        self.upvote_count = 0
