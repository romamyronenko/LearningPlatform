import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = str(os.getenv('DATABASE_URI'))


class TestConfig(Config):
    DEBUG = True
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
