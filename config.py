import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cb833909301b168a67c41af05c27452a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False