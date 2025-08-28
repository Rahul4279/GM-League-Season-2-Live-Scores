from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(50), unique=True, nullable=False)
    score_data = db.Column(db.String(120), nullable=False)
    is_live = db.Column(db.Boolean, default=True)