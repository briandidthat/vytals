from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(dotenv_path=path.join(basedir, '.env'))


class Config:
    """
      Base Configuration class will contain most of the basic configuration attributes and will be changed accordingly
      based on the environment.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = environ.get('SECRET_KEY')