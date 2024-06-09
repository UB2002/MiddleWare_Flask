from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(16), nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
