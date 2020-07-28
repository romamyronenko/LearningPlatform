import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://debian-sys-maint:' + str(os.getenv('DATABASE_PASSWORD')) + '@localhost/lplatform?charset=utf8mb4'


class TestConfig(Config):
    DEBUG = True
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
