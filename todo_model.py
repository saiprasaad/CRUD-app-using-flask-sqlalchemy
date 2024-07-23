from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    todos = db.relationship('Todo', backref='user', lazy = False)
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(100))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __init__(self, text, userid):
        self.text = text
        self.userid = userid
    