import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gmu_score.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False