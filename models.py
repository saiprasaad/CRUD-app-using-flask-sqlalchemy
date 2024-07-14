from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Student(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    hobbies = db.Column(db.String(100))
    country = db.Column(db.String(100))
    def __init__(self, name, email, password, gender, hobbies, country):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.hobbies = hobbies
        self.country = country
